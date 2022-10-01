from pathlib import Path
import yaml
from typing import Dict, List
from k8spurifier.frontend.parsers.abstractparser import ApplicationParser
from k8spurifier.frontend.repositories import Repository
from k8spurifier.applicationobject import ApplicationObject


class KubernetesConfigParser(ApplicationParser):
    """
    The kubernetes config parser class provides a parses that turns
    kubernetes config file into application objects.
    Since the yaml syntax allows multiple objects to be specified in one file,
    the parse() method returns one ApplicationObject per yaml document.

    The parsed application objects will have type "kubernetes_config"
    Also they will contain inside their data field:
    - document_number: the document number inside the yaml file
    - referenced_images: list of container images referenced by the kubernetes config
    """

    def __init__(self, context: Repository, kubernetes_config_file: Path):
        self.context = context
        self.context_path = context.get_local_path()
        self.config_file: Path = kubernetes_config_file

    def parse(self) -> List[ApplicationObject]:
        """Parse the kubernetes config file into (possibly multiple) application objects"""

        # resolve the config path
        kubernetes_config = (
            self.context_path/self.config_file).resolve().absolute()

        # load all the documents
        with open(kubernetes_config, 'r') as f:
            kubernetes_objects = list(yaml.safe_load_all(f.read()))

        out_objects = []
        for i, document in enumerate(kubernetes_objects):
            # compute referenced images for the document
            referenced_images = self.__get_referenced_images(document)

            # generate the application object
            out_objects.append(ApplicationObject(
                'kubernetes_config', self.config_file, data={
                    'document_number': i,
                    'referenced_images': referenced_images
                }))
        return out_objects

    def __get_referenced_images(self, document: Dict) -> List[str]:
        """
        Get all the referenced images by a kubernetes object
        """

        def get_all_containers(object):
            """
            Recursively traverse the document searching for
            container entries
            """
            if not isinstance(object, dict):
                return
            for k, v in object.items():
                if k == 'containers':
                    yield v
                elif isinstance(v, list):
                    for element in v:
                        for r in get_all_containers(element):
                            yield r
                elif isinstance(v, dict):
                    for r in get_all_containers(v):
                        yield r

        referenced_images = []
        for containers_object in get_all_containers(document):
            for container in containers_object:
                if 'image' in container:
                    referenced_images.append(container['image'])
        return referenced_images
