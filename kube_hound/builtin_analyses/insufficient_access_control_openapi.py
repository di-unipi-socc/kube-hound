from typing import Dict, List, Mapping, Optional
from kube_hound.analysis import AnalysisResult, StaticAnalysis

from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell


class InsufficientAccessControlOpenAPI(StaticAnalysis):
    analysis_id = 'openapi_iac'
    analysis_name = 'Insufficient Access Control in OpenAPI Analysis'
    analysis_description = 'find IAC smell in microservices API specifications'
    input_types = ['openapi']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        assert 'openapi' in input_objects
        openapi_objects = input_objects['openapi']

        out_smells = []
        for obj in openapi_objects:
            document: Dict = obj.get_content()
            service_prop = obj.service_properties

            # if SecuritySchemes component is not specified, return IAC smell
            if 'components' not in document or 'securitySchemes' not in document['components']:
                description = f"SecurityScheme not specified in {obj.path.name}"
                out_smells.append(self.__get_output_iac(description, service_prop))
                continue

            global_security = document.get('security')

            security_schemes = document['components']['securitySchemes']

            # interate through all paths, and all API methods
            for path in document['paths']:
                path_description = document['paths'][path]
                for method in path_description:
                    endpoint_description = path_description[method]

                    # run the analyis in the endpoint
                    result = self.__analyze_endpoint(
                        method, path, endpoint_description, security_schemes,
                        global_security, obj.path.name, service_prop)

                    if result is not None:
                        out_smells.append(result)

        return out_smells

    def __analyze_endpoint(self, method, path, endpoint_description,
                           security_schemes, global_security, object_name,
                           service_prop) -> Optional[AnalysisResult]:

        # get the security field and default to the global one if not found
        security = endpoint_description.get('security')
        if security is None:
            security = global_security

        # if the endpoint has no security field, then output the IAC smell
        if security is None:
            description = f"No security field specified in {object_name}, {method} {path}"
            return self.__get_output_iac(description, service_prop)

        # if security field is empty, output the IAC smell
        if security == []:
            description = f"Empty field specified in {object_name}, {method} {path}"
            return self.__get_output_iac(description, service_prop)

        # no smells detected
        return None

    def __service_is_external(self, properties):
        """
        Returns True is the service is declared as external,
        based on the service properties
        """
        if properties is None:
            return False

        return properties.get('external') is True

    def __get_output_iac(self, description, properties):
        if self.__service_is_external(properties):
            smells = {Smell.IAC}
        else:
            smells = {Smell.IAC, Smell.CA}
        
        return AnalysisResult(description, smells)