import abc
from typing import List, Set


class AnalysisResult:
    description = ''
    smells_detected: Set[str]

    def __init__(self):
        pass


class Analysis(metaclass=abc.ABCMeta):

    @ abc.abstractmethod
    def run_analysis(self) -> List[AnalysisResult]: pass
