from typing import List, Mapping
from kube_hound.analysis import AnalysisResult, DynamicAnalysis
from loguru import logger

from kube_hound.applicationobject import ApplicationObject
from kubernetes import client

from kube_hound.smells import Smell


class ExposedServicesWithExternalIp(DynamicAnalysis):
    analysis_id = 'external_ip'
    analysis_name = 'Exernal-IP analysis'
    analysis_description = 'detect exposed services by analysing the External-IP field for services'
    input_types: List[str] = ['kubernetes_config']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        kubernetes_configs = input_objects['kubernetes_config']

        # compute services mappings to claimed properties
        services_mapping = {}
        for document in kubernetes_configs:
            manifest_data = document.get_content()
            if manifest_data.get('kind') == 'Service':
                service_name = manifest_data['metadata']['name']
                service_properties = document.service_properties

                services_mapping[service_name] = service_properties

        output_smells = []

        # retrieve all services on the cluster
        namespace = 'default'
        v1 = client.CoreV1Api()
        ret = v1.list_namespaced_service(namespace, watch=False)

        # get services metadata
        data = ret.to_dict()
        data = data.get('items')
        if data is None:
            return []

        for service in data:
            service_name = service['metadata']['name']
            logger.debug(f"checking service {service_name}")

            # retrieve the status of the service
            status = service['status']
            load_balancer_status = status.get(
                'load_balancer').get('ingress')

            if load_balancer_status is not None and len(load_balancer_status) > 0:
                # load balancer has been detected
                properties = services_mapping.get(service_name)

                # get if the service is supposed to be external.
                # If no service with that name is specified in the config file,
                # the defaults to not external (i.e. undeclared exposed services will be reported)
                if properties is None:
                    external = False
                else:
                    external = properties.get('external')

                # skip the service if is declared as external
                if external is True:
                    continue

                # retrieve ip and host of the loadbalancer
                load_balancer_info = load_balancer_status[0]
                ip = load_balancer_info.get('ip')
                host = load_balancer_info.get('host')

                # report the smell
                description = f"External service detected: {service_name}\n" +\
                    f"exposed on external ip {ip if ip is not None else 'unknown'}, " +\
                    f"on host {host if host is not None else 'unknown'}"

                output_smells.append(
                    AnalysisResult(description, {Smell.PAM}))

        return output_smells
