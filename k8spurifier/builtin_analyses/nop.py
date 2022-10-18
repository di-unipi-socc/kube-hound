from typing import List, Mapping
from k8spurifier.analysis import Analysis, AnalysisResult
from loguru import logger

from k8spurifier.applicationobject import ApplicationObject
from k8spurifier.smells import Smell


class NopAnalysis(Analysis):
    analysis_id = 'S0'
    analysis_name = 'NOP analysis'
    input_types = ['kubernetes_config', 'dockerfile', 'openapi']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) -> List[AnalysisResult]:
        logger.info('running NOP analysis...')

        for key in input_objects:
            for obj in input_objects[key]:
                logger.debug(
                    f'NOP analysis received object of type {key}: {obj}')

        logger.info('finished NOP analyis')

        # testing results
        return [
            AnalysisResult('description 1', {Smell.CA}),
            AnalysisResult('description 2', {Smell.CA, Smell.NEDE})
        ]
