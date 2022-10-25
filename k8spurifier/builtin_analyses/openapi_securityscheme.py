from typing import Dict, List, Mapping
from k8spurifier.analysis import AnalysisResult, StaticAnalysis
from loguru import logger


from k8spurifier.applicationobject import ApplicationObject
from k8spurifier.smells import Smell


class SecuritySchemesAnalysis(StaticAnalysis):
    analysis_id = 'S0'
    analysis_name = 'SecurityScheme analysis'
    analysis_description = 'find unsecured endpoints in microservices API specifications'
    input_types = ['openapi']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) -> List[AnalysisResult]:

        assert 'openapi' in input_objects
        openapi_objects = input_objects['openapi']

        out_results = []
        for obj in openapi_objects:
            document: Dict = obj.get_content()
            service_prop = obj.service_properties

            # check if security schemes are specified
            if 'components' not in document or 'securitySchemes' not in document['components']:
                description = f"SecurityScheme not specified in {obj.path.name}"
                out_results.append(AnalysisResult(description, {Smell.IAC}))
                continue

            security_schemes = document['components']['securitySchemes']
            print(security_schemes)

            for path in document['paths']:
                path_description = document['paths'][path]
                for method in path_description:
                    endpoint_description = path_description[method]

                    print(endpoint_description)

                    security = endpoint_description.get('security')

                    # if the endpoint has no security field, then
                    if security is None:
                        description = f"No security field specified in {obj.path.name}, {method} {path}"
                        out_results.append(AnalysisResult(
                            description, {Smell.IAC}))
                        continue

                    print(security)

                    schemes = []
                    for x in security:
                        for k in x:
                            schemes.append(k)

                    for scheme in schemes:
                        scheme_desc: Dict = security_schemes.get(scheme)

                        # TODO logging invalid openAPI specification
                        if scheme_desc is not None and service_prop is not None:
                            is_basic_auth = scheme_desc.get(
                                'type') == 'http' and scheme_desc.get('scheme') == 'basic'
                            if is_basic_auth and not (service_prop.get('external') is True
                                                      or service_prop.get('performsAuthorization') is True):
                                description = f"Detected basic http authorization in {obj.path.name}, {method} {path}"
                                out_results.append(AnalysisResult(
                                    description, {Smell.MUA, Smell.CA}))

                    # basic auth: OK exposed or performsAuthentication

        return out_results
