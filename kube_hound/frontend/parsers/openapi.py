import json
from pathlib import Path
from typing import List
from kube_hound.applicationobject import ApplicationObject
from kube_hound.frontend.parsers.abstractparser import ApplicationParser
from kube_hound.frontend.repositories import Repository
from loguru import logger
import yaml


class OpenAPIParser(ApplicationParser):
    """
    The OpenAPIParser class provides a parses that turns
    openAPI specifications into application objects.
    """

    def __init__(self, context: Repository, path: Path):
        self.context = context
        self.context_path = context.get_local_path()
        self.path: Path = path

    def parse(self) -> List[ApplicationObject]:
        """Parse an openAPI specification into an ApplicationObject"""
        openapi_path = (
            self.context_path/self.path).resolve().absolute()
        if not openapi_path.exists():
            logger.warning(
                f'The openAPI specification {openapi_path} does not exists, skipping')
            return []

        f = open(openapi_path)
        if openapi_path.name.endswith('yaml'):
            document = yaml.safe_load(f)
        elif openapi_path.name.endswith('json'):
            document = json.load(f)
        else:
            logger.warning(f"{openapi_path}: file format not recognized")
            return []

        return [ApplicationObject('openapi', openapi_path, data={
            'cache': document
        })]
