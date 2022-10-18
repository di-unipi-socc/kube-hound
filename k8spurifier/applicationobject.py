from pathlib import Path


class ApplicationObject():
    """
    Application Object

    An application object is any object in the application object tree
    """

    def __init__(self, type: str, path: Path, data={}) -> None:
        self.type = type
        self.path = path
        self.data = data
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
            (f", {self.data}" if self.data != {} else "") + ")"
