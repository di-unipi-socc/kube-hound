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

    def __init__(self, context: Repository, path: Path):
        self.context = context
        self.context_path = context.get_local_path()
        self.path: Path = path

    def parse(self) -> List[ApplicationObject]:
        """Parse the sourcecode into an ApplicationObject"""
        sourcecode_path = (
            self.context_path/self.path).resolve().absolute()
        if not sourcecode_path.exists():
            return []

        return [ApplicationObject('sourcecode', sourcecode_path, data={})]
