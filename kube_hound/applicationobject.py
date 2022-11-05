from typing import Dict
from pathlib import Path
from typing import Optional


class ApplicationObject():
    """
    Application Object

    An application object is any object in the application object tree
    """

    def __init__(self, type: str, path: Path, data={}) -> None:
        self.type = type
        self.path = path
        self.data = data
        self.service_properties: Optional[Dict] = None
        # TODO better UUID?
        self.uuid = f'[{type}]-[{path}]'

    def get_uuid(self) -> str:
        return self.uuid

    def get_content(self):
        if 'cache' not in self.data:
            with open(self.path, 'r') as f:
                self.data['cache'] = f.read()

        return self.data['cache']

    def __repr__(self) -> str:
        return f"ApplicationObject({self.type}, {self.path.name}" + \
            (f", {self.service_properties}" if self.service_properties != '' else "") + ")" + \
            (f", {self.data}" if self.data != {} else "") + ")"
