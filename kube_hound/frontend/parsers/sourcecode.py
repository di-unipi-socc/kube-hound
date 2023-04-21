from pathlib import Path
from kube_hound.applicationobject import ApplicationObject
from kube_hound.frontend.parsers.abstractparser import ApplicationParser
from kube_hound.frontend.repositories import Repository
from typing import List



class SourcecodeParser(ApplicationParser):
    """
    The SourcecodeParser class provides a parser that turns
    a folder containing sourcecode to be analyzed into application objects.

    All ApplicationObject generated have type "sourcecode"
    """

    def __init__(self, context: Repository,path: Path, name: str ):
        self.context = context
        self.name = name
        self.context_path = context.get_local_path()
        self.path: Path = path

    def parse(self) -> List[ApplicationObject]:

        name = self.name
        path = self.path


        return [ApplicationObject('sourcecode', path, name)]
