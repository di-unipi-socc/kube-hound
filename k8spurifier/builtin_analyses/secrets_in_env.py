from typing import Dict, List, Mapping
from k8spurifier.analysis import AnalysisResult, DynamicAnalysis
from loguru import logger

from k8spurifier.applicationobject import ApplicationObject
from k8spurifier.smells import Smell
from kubernetes import client
from kubernetes.stream import stream
from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings


class SecretsInEnvironmentAnalysis(DynamicAnalysis):
    analysis_id = 'D0'
    analysis_name = 'Secrets in environment variables analysis'
    analysis_description = 'detect hardcoded secrets in containers environment'
    input_types: List[str] = []

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        output_results = []

        v1 = client.CoreV1Api()
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            pod_name = i.metadata.name
            for status in i.status.container_statuses:
                container_name = status.name
                logger.debug(
                    f'checking pod {pod_name}, container {container_name}')
                # print(container_name)
                command = ['env']
                response = stream(v1.connect_get_namespaced_pod_exec,
                                  pod_name,
                                  container=container_name,
                                  namespace=i.metadata.namespace,
                                  command=command,
                                  stderr=True, stdin=False,
                                  stdout=True, tty=False)
                # print(response)

                with open('/tmp/.env', 'w') as f:
                    f.write(response)

                secrets = SecretsCollection()
                with default_settings():
                    secrets.scan_file('/tmp/.env')

                result = secrets.json()
                if '/tmp/.env' in result:
                    secrets_found: List[Dict] = result['/tmp/.env']

                    for entry in secrets_found:
                        variable_name: str = response.split(
                            '\n')[int(entry['line_number']) - 1]

                        description = f"Detected secret in pod {pod_name} " +\
                            f", container {container_name}\n" +\
                            f"variable: {variable_name}\nreason: {entry['type']}"

                        output_results.append(
                            AnalysisResult(description, {Smell.HS}))

        return output_results
