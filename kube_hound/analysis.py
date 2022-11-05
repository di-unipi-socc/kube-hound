import abc
from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell
from typing import List, Mapping, Set


class AnalysisResult:
    def __init__(self, description: str, smells_detected: Set[Smell]):
        self.description = description
        self.smells_detected = smells_detected
        self.generating_analysis: str = ''

    def __repr__(self) -> str:
        return f"AnalysisResult({self.generating_analysis}," + \
            f" {self.description}, {self.smells_detected})"


class Analysis(abc.ABC):
    @property
    @abc.abstractmethod
    def analysis_name(self) -> str: pass

    @property
    @abc.abstractmethod
    def analysis_description(self) -> str: pass

    @property
    @abc.abstractmethod
    def analysis_id(self) -> str: pass

    @ abc.abstractmethod
    def run_analysis(
        self, input_objects: Mapping[str, List[ApplicationObject]]) -> List[AnalysisResult]: pass

    @property
    @abc.abstractmethod
    def input_types(self) -> List[str]: pass

    def __repr__(self) -> str:
        return f"Analysis({self.analysis_id}, {self.analysis_name})"


class StaticAnalysis(Analysis):
    pass


class DynamicAnalysis(Analysis):
    pass
