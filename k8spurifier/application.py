from pathlib import Path
from k8spurifier.frontend.config import ApplicationConfig
from k8spurifier.frontend.parsers.docker import DockerfileParser
from k8spurifier.frontend.parsers.kubernetes import KubernetesConfigParser
from loguru import logger
from k8spurifier.frontend.parsers.openapi import OpenAPIParser


class Application:
    def __init__(self, context_path: Path) -> None:
        self.context_path = context_path

    def set_config_path(self, config_path) -> None:
        self.config_path = config_path

    def set_context_path(self, context_path):
        self.context_path = context_path

    def aquire_application(self):
        self.config = ApplicationConfig(self.context_path)
        self.config.load_config_from_file(self.config_path)
        self.repositories = self.config.acquire_application()

    def parse_application(self):
        logger.info('parsing the application...')
        application_objects = []

        deployment = self.config.deployment()

        # parse kubernetes config files
        if 'kubernetes' in deployment:
            kubernetes_config = deployment['kubernetes']
            repository = self.repositories[kubernetes_config['repository']]
            files = repository.get_artifacts_by_regex(
                kubernetes_config['glob'])
            for f in files:
                kubernetes_parser = KubernetesConfigParser(repository, f)
                kubernetes_objects = kubernetes_parser.parse()

                # append all the objects in the application objects list
                for obj in kubernetes_objects:
                    application_objects.append(obj)

        # parse the services
        services = self.config.services()
        for service in services:
            service_repository = self.repositories[service['repository']]

            if 'dockerfile' in service:
                # get the image name if it exists
                image_name = ''
                if 'image' in service:
                    image_name = service['image']

                # parse the dockerfile
                dockerfile_parser = DockerfileParser(
                    service_repository, service['dockerfile'], image_name=image_name)
                dockerfile_objects = dockerfile_parser.parse()
                for obj in dockerfile_objects:
                    application_objects.append(obj)

            if 'openapi' in service:
                openapi_path = service['openapi']
                openapi_parser = OpenAPIParser(
                    service_repository, openapi_path)
                openapi_objects = openapi_parser.parse()

                for obj in openapi_objects:
                    application_objects.append(obj)

        for obj in application_objects:
            logger.debug(obj)

        logger.info(
            f'finished parsing: {len(application_objects)} resulting objects')
