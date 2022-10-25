from typing import List, Mapping
from k8spurifier.analysis import AnalysisResult, DynamicAnalysis
from loguru import logger

from k8spurifier.applicationobject import ApplicationObject
from kubernetes import client

from k8spurifier.smells import Smell


class ExternalIpAnalysis(DynamicAnalysis):
    analysis_id = 'D0'
    analysis_name = 'Secrets in environment variables analysis'
    analysis_description = 'detect hardcoded secrets in containers environment'
    input_types: List[str] = ['kubernetes_config']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        kubernetes_configs = input_objects['kubernetes_config']

        services_mapping = {}

        for document in kubernetes_configs:
            manifest_data = document.get_content()
            if manifest_data.get('kind') == 'Service':
                service_name = manifest_data['metadata']['name']
                service_properties = document.service_properties

                services_mapping[service_name] = service_properties
        output_results = []

        v1 = client.CoreV1Api()
        ret = v1.list_service_for_all_namespaces(watch=False)

        data = ret.to_dict()
        data = data.get('items')
        if data is None:
            return []

        for service in data:
            service_name = service['metadata']['name']

            status = service['status']
            load_balancer_status = status.get(
                'load_balancer').get('ingress')
            if load_balancer_status is not None:
                if service_name in services_mapping:
                    logger.debug(f"checking service {service_name}")
                    properties = services_mapping[service_name]
                    if properties is None:
                        continue
                    external = properties.get('external')
                    if external is False:
                        description = f"External service detected: {service_name}\n" +\
                            f"exposed on external ip {load_balancer_status.get('ip')}" +\
                            f"on host {load_balancer_status.get('host')}"

                    output_results.append(
                        AnalysisResult(description, {Smell.PAM}))
            # print(data[service])
        return output_results
