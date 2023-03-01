from typing import Dict, List, Mapping, Optional
from kube_hound.analysis import AnalysisResult, StaticAnalysis
from loguru import logger


from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell


class MultipleUserAuthenticationOpenAPI(StaticAnalysis):
    analysis_id = 'openapi_mua'
    analysis_name = 'Multiple User Authentication in OpenAPI Analysis'
    analysis_description = 'find multiple authentication endpoints in microservices API specifications'
    input_types = ['openapi']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        self.authentication_endpoints = []

        assert 'openapi' in input_objects
        openapi_objects = input_objects['openapi']

        for obj in openapi_objects:
            document: Dict = obj.get_content()
            service_prop = obj.service_properties

            # if SecuritySchemes component is not specified, ignore
            if 'components' not in document or 'securitySchemes' not in document['components']:
                continue

            global_security = document.get('security')

            security_schemes = document['components']['securitySchemes']

            # interate through all paths, and all API methods
            for path in document['paths']:
                path_description = document['paths'][path]
                for method in path_description:
                    endpoint_description = path_description[method]

                    # run the analyis in the endpoint
                    self.__analyze_endpoint(
                        method, path, endpoint_description, security_schemes,
                        global_security, obj.path.name, service_prop)

        # if multiple authentication endpoints have been detected, report MUA smell
        if len(self.authentication_endpoints) >= 2:
            description = "Multiple user authentication endpoints:\n- " + '\n- '.join(self.authentication_endpoints)
            return [AnalysisResult(description, {Smell.MUA})]
        return []

    def __analyze_endpoint(self, method, path, endpoint_description,
                           security_schemes, global_security, object_name,
                           service_prop) -> Optional[AnalysisResult]:

        # get the security field and default to the global one if not found
        security = endpoint_description.get('security')
        if security is None:
            security = global_security

        if security is None or security == []:
            return

        # iterate through all security schemes declared for this endpoint
        schemes = self.__get_schemes(security)
        for scheme in schemes:
            scheme_info: Dict = security_schemes.get(scheme)

            # if the is not described in the SecuritySchemes component,
            # we throw a warning to the user
            if scheme_info is None:
                logger.warning(f'OpenAPI specification {object_name} is invalid, '
                               '{scheme} is not present in SecuritySchemes')
                continue

            # If the endpoint is enacting Basic authorization scheme, append it to the authentication
            # endpoints list
            if self.__is_basic_auth(scheme_info) \
                    and not self.__ignore_basic_auth(service_prop):
                description = f"Basic http authorization in {object_name}, {method} {path}"
                self.authentication_endpoints.append(description)

    def __get_schemes(self, security):
        """
        Get all schemes from the security field
        """
        schemes = []
        for x in security:
            for k in x:
                schemes.append(k)
        return schemes

    def __is_basic_auth(self, scheme):
        return scheme.get('type') == 'http' and \
            scheme.get('scheme') == 'basic'

    def __ignore_basic_auth(self, properties):
        """
        Returns True is the service can use Basic HTTP authorization,
        based on the service properties
        """
        if properties is None:
            return False

        return properties.get('performsAuthorization') is True

    def __service_is_external(self, properties):
        """
        Returns True is the service is declared as external,
        based on the service properties
        """
        if properties is None:
            return False

        return properties.get('external') is True

    # def __get_output_iac(self, description, properties):
    #     if self.__service_is_external(properties):
    #         smells = {Smell.IAC}
    #     else:
    #         smells = {Smell.IAC, Smell.CA}
        
    #     return AnalysisResult(description, {Smell.MUA, Smell.CA})