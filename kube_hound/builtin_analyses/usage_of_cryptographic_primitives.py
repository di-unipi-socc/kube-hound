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

from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell


class UsageOfCryptographicPrimitives(StaticAnalysis):
    analysis_id = 'crypto_primitive_usage'
    analysis_name = 'Usage of Cryptographic Primitives Analysis'
    analysis_description = ''
    input_types = ['sourcecode']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:
        assert 'sourcecode' in input_objects
        sourcecode_objects = input_objects['sourcecode']
        print(sourcecode_objects)

        self.docker_client = docker.from_env()

       
        # spawn a sonarqube container
        logger.debug('spawning sonarqube container')
        sonarqube_container = self.docker_client.containers.run(
            'sonarqube', detach=True, ports={'9000/tcp': 9000})

        # Access SonarQube through its exposed port
        sonarqube_url = 'http://localhost:9000'




        output_results = []



        try:
            self.wait_for_running_container(sonarqube_container)
            sleep(150)

            # Stop the container
            sonarqube_container.stop()

            # Remove the container
            sonarqube_container.remove()

        except requests.exceptions.RequestException as e:
            print("Error triggering analysis:", e)

        return []

    def wait_for_running_container(self, container):
        """
        Actively wait for a container to become running
        """
        timeout = 120
        stop_time = 0.5
        elapsed_time = 0

        while elapsed_time < timeout:
            sleep(stop_time)
            elapsed_time += stop_time
            container.reload()
            if container.status == 'running':
                return