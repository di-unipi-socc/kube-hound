import abc
from k8spurifier.applicationobject import ApplicationObject
from k8spurifier.smells import Smell
from typing import List, Mapping, Set


class AnalysisResult:
    def __init__(self, description: str, smells_detected: Set[Smell]):
        self.description = description
        self.smells_detected = smells_detected
        self.generating_analysis: str = ''

    def __repr__(self) -> str:
        return f"AnalysisResult({self.generating_analysis}," + \
            f" {self.description}, {self.smells_detected})"


class Analysis(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def analysis_name(self) -> str: pass

    @property
    @abc.abstractmethod
    def analysis_description(self) -> str: pass

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
