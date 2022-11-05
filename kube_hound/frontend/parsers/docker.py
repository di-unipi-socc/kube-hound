from pathlib import Path
from typing import List
from kube_hound.frontend.parsers.abstractparser import ApplicationParser
from kube_hound.frontend.repositories import Repository
from kube_hound.applicationobject import ApplicationObject


class DockerfileParser(ApplicationParser):
    """
    The DockerfileParser class provides a parses that turns
    Dockerfiles into application objects.

    If an image name is specified in the constructor, then it is added
    in the applicaiton object data under the image_name field.
    All ApplicationObject generated have type "dockerfile"
    """

    def __init__(self, context: Repository, path: Path, image_name=''):
        self.context = context
        self.context_path = context.get_local_path()
        self.path: Path = path
        self.image_name = image_name

    def parse(self) -> List[ApplicationObject]:
        """Parse a Dockerfile into an ApplicationObject"""
        dockerfile_path = (
            self.context_path/self.path).resolve().absolute()
        if not dockerfile_path.exists():
            # TODO logging
            return []

        return [ApplicationObject('dockerfile', dockerfile_path, data={
            'image_name': self.image_name
        })]
