from typing import List, Mapping
from k8spurifier.analysis import AnalysisResult, DynamicAnalysis
from loguru import logger

from k8spurifier.applicationobject import ApplicationObject
from kubernetes import client

from k8spurifier.smells import Smell


class ExternalIpAnalysis(DynamicAnalysis):
    analysis_id = 'external_ip'
    analysis_name = 'Exernal-IP analysis'
    analysis_description = 'detect exposed services by analysing the External-IP field for services'
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

        output_smells = []

        v1 = client.CoreV1Api()
        ret = v1.list_service_for_all_namespaces(watch=False)

        data = ret.to_dict()
        data = data.get('items')
        if data is None:
            return []

        for service in data:
            service_name = service['metadata']['name']
            logger.debug(f"checking service {service_name}")

            status = service['status']
            load_balancer_status = status.get(
                'load_balancer').get('ingress')
            if load_balancer_status is not None and len(load_balancer_status) > 0:
                if str(service_name) in services_mapping:
                    properties = services_mapping[service_name]

                    logger.debug(properties)
                    if properties is None:
                        external = False
                    else:
                        external = properties.get('external')

                    if external is True:
                        continue

                    load_balancer_info = load_balancer_status[0]
                    ip = load_balancer_info.get('ip')
                    host = load_balancer_info.get('host')

                    description = f"External service detected: {service_name}\n" +\
                        f"exposed on external ip {ip if ip is not None else 'unknown'}, " +\
                        f"on host {host if host is not None else 'unknown'}"

                    output_smells.append(
                        AnalysisResult(description, {Smell.PAM}))

        return output_smells
