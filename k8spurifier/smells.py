from typing import Mapping


class Smell:
    def __init__(self, identifier, description):
        self.identifier = identifier
        self.description = description


class SmellManager:

    def __init__(self):
        self._smells_collection: Mapping[str, Smell]

    def add_smell(self, smell):
        if smell.identifier in self._smells_collection:
            raise ExistingSmellIdError()

        self._smells_collection[smell.identifier] = smell


class ExistingSmellIdError(Exception):
    pass
