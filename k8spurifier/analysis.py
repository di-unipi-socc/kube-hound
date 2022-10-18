import abc
from k8spurifier.applicationobject import ApplicationObject
from typing import List, Mapping, Set


class AnalysisResult:
    description = ''
    smells_detected: Set[str]

    def __init__(self):
        pass


class Analysis(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def analysis_name(self) -> str: pass

    @property
    @abc.abstractmethod
    def analysis_id(self) -> str: pass

    @property
    @abc.abstractmethod
    def input_types(self) -> List[str]: pass

    @ abc.abstractmethod
    def run_analysis(
        self, input_objects: Mapping[str, List[ApplicationObject]]) -> List[AnalysisResult]: pass

    def __repr__(self) -> str:
        return f"Analysis({self.analysis_id}, {self.analysis_name})"
