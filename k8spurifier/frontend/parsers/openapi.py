from pathlib import Path
from typing import List
from k8spurifier.applicationobject import ApplicationObject
from k8spurifier.frontend.parsers.abstractparser import ApplicationParser
from k8spurifier.frontend.repositories import Repository
from loguru import logger


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

        return [ApplicationObject('openapi', openapi_path)]
