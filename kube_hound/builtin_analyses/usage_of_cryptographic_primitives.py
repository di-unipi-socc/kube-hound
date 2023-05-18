from pathlib import Path
from typing import Dict, List, Mapping, Optional
from time import sleep
from kube_hound.analysis import AnalysisResult, StaticAnalysis
from loguru import logger
import docker
import os
import requests
import json
import subprocess
from sonarqube import SonarQubeClient


from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell


class UsageOfCryptographicPrimitives(StaticAnalysis):
    analysis_id = 'sourcecode_ucp'
    analysis_name = 'Usage of Cryptographic Primitives Analysis'
    analysis_description = 'detect usage of cryptographic primitives inside the microservices sourcecode'
    input_types = ['sourcecode']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:
        assert 'sourcecode' in input_objects
        sourcecode_objects = input_objects['sourcecode']


        # build volume for sonarqube analysis
        paths = [str(sourcecode.path) for sourcecode in sourcecode_objects]
        volumes = {}
        for path in paths:
            volumes[path] = {
                'bind': '/usr/src' + path,
                'mode': 'rw'
            }

        self.docker_client = docker.from_env()

        url = 'http://localhost:9000'
        username = "admin"
        password = "admin"
        host_properties_path = str(Path('./custom-sonar.properties').absolute())
        container_properties_path = '/opt/sonarqube/conf/custom.properties'

        output_results = []

        #set project variables
        project_key = "my_project"
        project_name = "My Project"
        project_visibility = "public"
        auth = ("admin", "admin")

        #vaious enpoints that are needed
        api_endpoint_create = f"{url}/api/projects/create"      #to create project
        api_endpoint_create_token = f"{url}/api/user_tokens/generate"       #to generate user token
        api_endpoint_search = f"{url}/api/issues/search"
        sonar = SonarQubeClient(sonarqube_url=url, username=username, password=password)

        # spawn a sonarqube container
        logger.debug('spawning sonarqube container')
        sonarqube_container = self.docker_client.containers.run(
            'sonarqube', detach=True, ports={'9000/tcp': 9000}, volumes={host_properties_path: {'bind': container_properties_path, 'mode': 'ro'}})



        try:
            self.wait_for_running_container(sonarqube_container)
            logger.debug("Sonarqube container is now running")

            while True:
                container_logs = self.docker_client.containers.get(str(sonarqube_container.id)).logs().decode("utf-8")
                if "SonarQube is operational" in container_logs:
                    break

                sleep(1)  # Wait for 1 second before checking again

            logger.debug("Server is now running")

            sonar.auth.authenticate_user(login="admin", password="admin")
            sonar.auth.check_credentials()





            # Set the request payload with the required parameters
            payload = {
                "name": project_name,
                "project": project_key,
                "visibility": project_visibility,
            }

            # Send the POST request to create the project
            response = requests.post(api_endpoint_create, auth=auth, data=payload)

            # Check the response status code
            if response.status_code == 200:
                logger.debug("Sonarqube project created successfully.")
            else:
                logger.warning("Sonarqube project creation failed.")





            # Set the request payload with the required parameters
            payload = {
                'name': 'My Token',
                'login': 'admin',
            }

            # Send the POST request to create the user token
            response = requests.post(api_endpoint_create_token, auth=auth, data=payload)

            # Check the response status code
            if response.status_code == 200:
                data = response.json()
                token = str(data['token'])
            else:
                logger.warning('Failed to create the authentication token.')






            # Inspect the container
            container_info = self.docker_client.api.inspect_container(sonarqube_container.id)

            # Get the IP address from the container's network settings
            ip_address = container_info['NetworkSettings']['IPAddress']
            access_address = 'http://'+str(ip_address)+':9000'



            # spawn a sonarscanner container
            logger.debug('spawning sonarscanner container')
            sonarscanner_container = self.docker_client.containers.run(
                'sonarsource/sonar-scanner-cli',
                detach=True,
                volumes=volumes,
                environment={
                    'SONAR_HOST_URL': access_address,
                    'SONAR_SCANNER_OPTS': f'-Dsonar.projectKey={project_key} -Dsonar.token={token} -Dsonar.java.binaries=.',
                },
            )

            while True:
                sonarscanner_container.reload()
                if not sonarscanner_container.status == 'running':

                    break

                sleep(1)  # Wait for 1 second before checking again

            sleep(10)

            rule_keys = ["python:S5542", "php:S5542", "javascript:S5542", "kotlin:S5542", "java:S5542", "typescript:S5542"]

            # Parameters for the API request
            params = {
                "projectKey": project_key,
                "rules": ",".join(rule_keys),
            }


            # Send the authenticated API request
            response = requests.get(api_endpoint_search, params=params, auth=auth)

            # Check if the request was successful
            if response.status_code == 200:
                response_json = response.json()
                issues = response_json.get("issues", [])

                if issues:
                    for issue in issues:
                        component = issue["component"]
                        message = issue["message"]
                        line = issue["line"]
                        component = os.path.basename(component)
                        description = f"Sonarqube found potential problems in {component}\n" + \
                                      f"line: {line}\n" + \
                                      f"reason: {message}"

                        output_results.append(
                            AnalysisResult(description, {Smell.UCP}))
                else:
                    logger.info("No instances of usage of cryptographic primitves")
            else:
                logger.warning("Failed to retrieve issues.")




            # Stop the container

            sonarscanner_container.stop()

            # Remove the container
            sonarscanner_container.remove()


            # Stop the container
            sonarqube_container.stop()

            # Remove the container
            sonarqube_container.remove()

            return output_results
        except requests.exceptions.RequestException as e:
            logger.warning("Error triggering analysis:", e)

        return []

    def wait_for_running_container(self, container):
        """
        Actively wait for a container to become running
        """
        timeout = 50
        stop_time = 0.5
        elapsed_time = 0

        while elapsed_time < timeout:
            sleep(stop_time)
            elapsed_time += stop_time
            container.reload()
            if container.status == 'running':
                return