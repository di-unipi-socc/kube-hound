from pathlib import Path
from typing import Dict, List, Optional, Type
from kube_hound.analysis import Analysis, AnalysisResult
from kube_hound.scheduler import AnalysisScheduler
from kube_hound.applicationobject import ApplicationObject
from kube_hound.frontend.config import ApplicationConfig
from kube_hound.frontend.parsers.docker import DockerfileParser
from kube_hound.frontend.parsers.kubernetes import KubernetesConfigParser
from kube_hound.frontend.parsers.sourcecode import SourcecodeParser
from kube_hound.frontend.parsers.terraform import TerraformParser
from kube_hound.frontend.parsers.openapi import OpenAPIParser
from loguru import logger
from kube_hound.service import Service
from kubernetes import config
import json

class Hound:
    def __init__(self, context_path: Path) -> None:
        self.context_path = context_path
        self.application_objects: List[ApplicationObject] = []
        self.services: Dict[str, Service] = {}
        self.analysis_results: List[AnalysisResult] = []

        # flags to run analyses types
        self.run_static = True
        self.run_dynamic = True

        self.scheduler = AnalysisScheduler([])

    def set_config_path(self, config_path) -> None:
        self.config_path = config_path

    def set_context_path(self, context_path):
        self.context_path = context_path

    def aquire_application(self):
        self.config = ApplicationConfig(self.context_path)
        self.config.load_config_from_file(self.config_path)
        self.repositories = self.config.acquire_application()
        self.sourcecodes = self.config.acquire_sourcecodes(self.repositories)

    def parse_application(self):
        logger.info('parsing the application...')
        application_objects = []

        deployment = self.config.deployment()

        # parse the services
        config_services = self.config.services()

        # parse all services names
        for service_data in config_services:
            service_name = service_data['name']
            service = Service(service_name)
            self.services[service_name] = service

        # parse the service properties
        for service, properties in self.config.properties():
            self.services[service].properties = properties

        # parse kubernetes and terraform
        for keys in deployment:
            match keys:
                case 'kubernetes':
                    config = deployment['kubernetes']
                
                case 'terraform':
                    config = deployment['terraform']

                case _:
                    logger.info('Deployment {keys} not found')
                    continue
            
            repository = self.repositories[config['repository']]
            files = repository.get_artifacts_by_regex(config['glob'])
            for f in files:
                match keys:
                    case 'kubernetes':
                        kubernetes_parser = KubernetesConfigParser(
                            repository, f, self.services)
                        objects = kubernetes_parser.parse()
                
                    case 'terraform':
                        terraform_parser = TerraformParser(
                            repository, f, self.services)
                        objects = terraform_parser.parse()

                    case _:
                        continue
            
                for obj in objects:
                    application_objects.append(obj)

        # parse services' dockerfiles, openapis and sourcecodes
        dockerfiles: List[ApplicationObject] = []
        openapis: List[ApplicationObject] = []
        sourcecodes: List[ApplicationObject] = []
        for service_data in config_services:
            # TODO validation
            service_repository = self.repositories[service_data['repository']]
            service = self.services[service_data['name']]

            if 'dockerfile' in service_data:
                # get the image name if it exists
                image_name = ''
                if 'image' in service_data:
                    image_name = service_data['image']

                # parse the dockerfile
                dockerfile_parser = DockerfileParser(
                    service_repository, service_data['dockerfile'], image_name=image_name)
                dockerfile_objects = dockerfile_parser.parse()
                for obj in dockerfile_objects:
                    if service.properties is not None:
                        obj.service_properties = dict(service.properties)

                    dockerfiles.append(obj)

                if len(dockerfile_objects) > 0:
                    service.dockerfile = dockerfile_objects[0]

            if 'sourcecode' in service_data:
                service_name = service_data['name']
                local_path = Path(self.sourcecodes[service_name])
                logger.info(local_path)

                sourcecode_parser = SourcecodeParser(service_repository, local_path, service_name)

                sourcecode_objects = sourcecode_parser.parse()
                for obj in sourcecode_objects:
                    if service.properties is not None:
                        obj.service_properties = dict(service.properties)
                    logger.debug(obj)
                    sourcecodes.append(obj)

                if len(sourcecode_objects) > 0:
                    service.dockerfile = sourcecode_objects[0]

            if 'openapi' in service_data:
                openapi_path = service_data['openapi']
                openapi_parser = OpenAPIParser(
                    service_repository, openapi_path)
                openapi_objects = openapi_parser.parse()

                for obj in openapi_objects:
                    if service.properties is not None:
                        obj.service_properties = dict(service.properties)

                    openapis.append(obj)

                if len(openapi_objects) > 0:
                    service.dockerfile = openapi_objects[0]

        # deduplication of dockerfiles
        seen_openapis = set()
        for spec in dockerfiles:
            if spec.path not in seen_openapis:
                seen_openapis.add(spec.path)
                application_objects.append(spec)

        # deduplication of sourcecodes ---- Still needs to be worked on
        seen_sourcodes = set()
        for spec in sourcecodes:
            if spec.path not in seen_sourcodes:
                seen_sourcodes.add(spec.path)
                application_objects.append(spec)

        # deduplication of openapi specifications
        seen_openapis = set()
        for spec in openapis:
            if spec.path not in seen_openapis:
                seen_openapis.add(spec.path)
                application_objects.append(spec)

        for obj in application_objects:
            logger.debug(obj)

        self.application_objects = application_objects

        logger.info(
            f'finished parsing: {len(application_objects)} resulting objects')

    def get_service(self, service_name: str) -> Optional[Service]:
        if service_name in self.services:
            return self.services[service_name]
        return None

    def load_kubernetes_cluster_config(self):
        # TODO add configuration path setting
        logger.info('Trying to load the kubernetes cluster config')
        try:
            config.load_kube_config()
        except Exception:
            logger.warning(
                'failed to load kubernetes config, ignoring dynamic analyses')
            self.run_dynamic = False
        logger.info('Successfully loaded kubernetes cluster config')

    def run_analyses(self, analysis_list=None):
        logger.info('running analyses on the application')

        self.scheduler.set_application_objects(self.application_objects)

        if analysis_list != None:
            self.scheduler.analysis_list = analysis_list

        self.analysis_results = self.scheduler.run_analyses(
            self.run_static, self.run_dynamic)

    def show_results(self, json_output=False):
        if json_output:
            output_obj = []
            for result in self.analysis_results:
                output_obj.append({
                    'analysis': result.generating_analysis,
                    'smells': list(map(repr, result.smells_detected)),
                    'description': result.description
                })
            print(json.dumps(output_obj))
        else:
            print('Analysis results:')
            for result in self.analysis_results:
                description_formatted = '\t' + \
                    '\n\t'.join(result.description.split('\n'))
                print(f"{result.generating_analysis} - detected smells {result.smells_detected}\n"
                      f"{description_formatted}\n")

    def register_analysis(self, analysis: Type[Analysis]):
        self.scheduler.register_analysis(analysis)