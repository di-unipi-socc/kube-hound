from typing import Dict, List, Mapping
from k8spurifier.analysis import AnalysisResult
from k8spurifier.applicationobject import ApplicationObject
from k8spurifier.builtin_analyses import all_analyses
from loguru import logger


class AnalysisScheduler():
    def __init__(self, application_objects: List[ApplicationObject]):
        self.application_objects = application_objects
        self.object_type_mapping = self.__compute_type_mapping(
            application_objects)

        # TODO naming is a bit confusing
        self.analyses = all_analyses

    def __compute_type_mapping(self, objects: List[ApplicationObject]) \
            -> Mapping[str, List[ApplicationObject]]:
        resulting_mapping: Dict[str, List[ApplicationObject]] = {}

        for obj in objects:
            if obj.type in resulting_mapping:
                resulting_mapping[obj.type].append(obj)
            else:
                resulting_mapping[obj.type] = [obj]

        return resulting_mapping

    def run_analyses(self) -> List[AnalysisResult]:
        for analysis_class in self.analyses:
            analysis = analysis_class()

            input_objects = {}
            for type in analysis_class.input_types:

                if type in self.object_type_mapping:
                    input_objects[type] = self.object_type_mapping[type]
                else:
                    input_objects[type] = []
                    logger.warning(f'analysis "{analysis_class.analysis_name}" required objects '
                                   'of type {type} but no one exists in the application')
            logger.info(f'Running "{analysis_class.analysis_name}"')
            analysis.run_analysis(input_objects)
            logger.info(f'Finished "{analysis_class.analysis_name}"')

        # TODO analysis collection
        return []
