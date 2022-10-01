from typing import List, Mapping
from k8spurifier.analysis import Analysis, AnalysisResult
from loguru import logger

from k8spurifier.applicationobject import ApplicationObject


class NopAnalysis(Analysis):
    analysis_id = 'S0'
    analysis_name = 'NOP: do nothing'
    input_types = ['kubernetes_config', 'dockerfile', 'openapi']

    def run_analysis(self, input_objects: Mapping[str, ApplicationObject]) -> List[AnalysisResult]:
        logger.info('running NOP analysis...')

        for key in input_objects:
            for obj in input_objects[key]:
                logger.debug(
                    f'NOP analysis received object of type {key}: {obj}')

        logger.info('finished NOP analyis')
        return []
