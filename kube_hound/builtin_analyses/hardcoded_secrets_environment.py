from typing import Dict, List, Mapping
from kube_hound.analysis import AnalysisResult, DynamicAnalysis
from loguru import logger

from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell
from kubernetes import client
from kubernetes.stream import stream

from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings

TMP_FILENAME = '/tmp/.env'


class HardcodedSecretsInEnvironment(DynamicAnalysis):
    analysis_id = 'secrets_in_env'
    analysis_name = 'Secrets in environment variables analysis'
    analysis_description = 'detect hardcoded secrets in containers environment'
    input_types: List[str] = []

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        output_results = []

        # get all running pods in the cluter
        v1 = client.CoreV1Api()
        ret = v1.list_pod_for_all_namespaces(watch=False)

        for i in ret.items:
            pod_name = i.metadata.name
            for status in i.status.container_statuses:
                container_name = status.name
                logger.debug(
                    f'checking pod {pod_name}, container {container_name}')
                try:
                    # retrieve the enviroment on the container
                    command = ['env']
                    response = stream(v1.connect_get_namespaced_pod_exec,
                                      pod_name,
                                      container=container_name,
                                      namespace=i.metadata.namespace,
                                      command=command,
                                      stderr=True, stdin=False,
                                      stdout=True, tty=False)
                except:
                    logger.warning(
                        f'checking for environment variables of pod {pod_name}, container {container_name} failed')
                    continue

                # surround the variable values with double quotes
                # this gives better results in secrets detection
                quoted_env_content = ''
                for line in response.split('\n'):
                    toks = line.split('=', 1)
                    if len(toks) != 2:
                        quoted_env_content += line + '\n'
                        continue

                    quoted_env_content += f'{toks[0]}="{toks[1]}"\n'

                with open(TMP_FILENAME, 'w') as f:
                    f.write(quoted_env_content)

                # create a new SecretCollection object, to detect secrets
                secrets = SecretsCollection()

                # scan the retrieved environment
                with default_settings():
                    secrets.scan_file(TMP_FILENAME)

                # retrieve all the found secrets
                result = secrets.json()
                if TMP_FILENAME in result:
                    secrets_found: List[Dict] = result[TMP_FILENAME]

                    for entry in secrets_found:
                        variable_name: str = response.split(
                            '\n')[int(entry['line_number']) - 1]

                        # obfuscate value to not accidentally expose in the output
                        toks = variable_name.split('=', 1)
                        if len(toks) != 2:
                            variable_output = variable_name
                        else:
                            variable_output =\
                                f"{toks[0]}={toks[1][:4]}{'*' * max(0, len(toks[1])-4)}"

                        # report the smell
                        description = f"Detected secret in pod {pod_name}" +\
                            f", container {container_name}\n" +\
                            f"variable: {variable_output}\nreason: {entry['type']}"

                        output_results.append(
                            AnalysisResult(description, {Smell.HS}))

        return output_results
