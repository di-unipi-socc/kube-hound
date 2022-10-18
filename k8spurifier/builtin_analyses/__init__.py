from typing import List, Type
from k8spurifier.analysis import Analysis
from k8spurifier.builtin_analyses.nop import NopAnalysis

all_analyses: List[Type[Analysis]] = [
    NopAnalysis
]
