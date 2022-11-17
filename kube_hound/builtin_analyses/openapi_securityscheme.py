from typing import Dict, List, Mapping, Optional
from kube_hound.analysis import AnalysisResult, StaticAnalysis
from loguru import logger


from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell


class SecuritySchemesAnalysis(StaticAnalysis):
    analysis_id = 'openapi_securityscheme'
    analysis_name = 'SecurityScheme analysis'
    analysis_description = 'find unsecured endpoints in microservices API specifications'
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
                out_smells.append(AnalysisResult(description, {Smell.IAC}))
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
            return AnalysisResult(description, {Smell.IAC})

        # if security field is empty, output the IAC smell
        if security == []:
            description = f"Empty field specified in {object_name}, {method} {path}"
            return AnalysisResult(description, {Smell.IAC})

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

            # If the endpoint is enacting Basic authorization scheme, and it shouldn't,
            # output the CA and MUA smells
            if self.__is_basic_auth(scheme_info) \
                    and not self.__service_can_use_basic_auth(service_prop):
                description = f"Detected basic http authorization in {object_name}, {method} {path}"
                return AnalysisResult(description, {Smell.MUA, Smell.CA})

        # no smells detected
        return None

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

    def __service_can_use_basic_auth(self, properties):
        """
        Returns True is the service can use Basic HTTP authorization,
        based on the service properties
        """
        if properties is None:
            return False

        return properties.get('external') is True or \
            properties.get('performsAuthorization') is True
