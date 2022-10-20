from typing import Dict, List, Mapping
from k8spurifier.analysis import Analysis, AnalysisResult, DynamicAnalysis, StaticAnalysis
from loguru import logger

from k8spurifier.applicationobject import ApplicationObject
from k8spurifier.smells import Smell
from kubernetes import client, config
from kubernetes.stream import stream


class SecretsInEnvironmentAnalysis(DynamicAnalysis):
    analysis_id = 'D0'
    analysis_name = 'Secrets in environment analysis'
    analysis_description = 'detect hardcoded secrets in containers environment'
    input_types = []

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        v1 = client.CoreV1Api()
        #print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            for status in i.status.container_statuses:
                container_name = status.name
                # print(container_name)
                command = ['env']
                response = stream(v1.connect_get_namespaced_pod_exec,
                                  i.metadata.name,
                                  container=container_name,
                                  namespace=i.metadata.namespace,
                                  command=command,
                                  stderr=True, stdin=False,
                                  stdout=True, tty=False)
                print(response)

        return []
