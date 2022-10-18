from typing import Dict
from typing import Optional

from k8spurifier.applicationobject import ApplicationObject


class Service:
    def __init__(self, name: str):
        self.name = name
        self.dockerfile: Optional[ApplicationObject] = None
        self.openapi: Optional[ApplicationObject] = None
        self.properties: Dict = {}

    def __repr__(self) -> str:
        return f"Service({self.name}, {self.properties})"
