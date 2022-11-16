from typing import Dict, List, Mapping, Optional, Type
from kube_hound.analysis import Analysis, AnalysisResult, DynamicAnalysis, StaticAnalysis
from kube_hound.applicationobject import ApplicationObject
from kube_hound.builtin_analyses import all_analyses
from loguru import logger


class AnalysisScheduler():
    def __init__(self, application_objects: List[ApplicationObject] = []):
        self.application_objects = application_objects
        self.object_type_mapping = self.__compute_type_mapping(
            application_objects)
        self.analysis_list: Optional[List[str]] = None

        # TODO naming is a bit confusing
        self.analyses: List[Type[Analysis]] = all_analyses

    def __compute_type_mapping(self, objects: List[ApplicationObject]) \
            -> Mapping[str, List[ApplicationObject]]:
        resulting_mapping: Dict[str, List[ApplicationObject]] = {}

        for obj in objects:
            if obj.type in resulting_mapping:
                resulting_mapping[obj.type].append(obj)
            else:
                resulting_mapping[obj.type] = [obj]

        return resulting_mapping

    def set_application_objects(self, application_objects: List[ApplicationObject]):
        self.application_objects = application_objects
        self.object_type_mapping = self.__compute_type_mapping(
            application_objects)

    def register_analysis(self, analysis: Type[Analysis]):
        self.analyses.append(analysis)
        logger.info(f"analysis {analysis.analysis_name} registered")

    def run_analyses(self, run_static: bool, run_dynamic: bool) -> List[AnalysisResult]:
        total_analysis_results = []
        for analysis_class in self.analyses:
            if not run_static and issubclass(analysis_class, StaticAnalysis):
                continue

            if not run_dynamic and issubclass(analysis_class, DynamicAnalysis):
                continue

            if self.analysis_list is not None and \
                    analysis_class.analysis_id not in self.analysis_list:
                continue

            analysis_obj = analysis_class()

            input_objects = {}
            object_count = 0
            for inp_type in analysis_class.input_types:  # type: ignore
                if inp_type in self.object_type_mapping:
                    input_objects[inp_type] = self.object_type_mapping[inp_type]
                    object_count += len(self.object_type_mapping[inp_type])
                else:
                    input_objects[inp_type] = []
                    logger.warning(f'analysis "{analysis_class.analysis_name}" required objects '
                                   f'of type {inp_type} but no one exists in the application')

            if len(analysis_class.input_types) > 0 and object_count == 0:
                logger.info(f'Skipping analysis"{analysis_class.analysis_name} because there are'
                            ' no input objects')
                continue
            logger.info(f'Running "{analysis_class.analysis_name}"')
            analysis_results = analysis_obj.run_analysis(input_objects)

            # inject generating analysis name
            # and append to the aggregate list
            analysis_name = analysis_obj.analysis_name
            for result in analysis_results:
                result.generating_analysis = analysis_name
                total_analysis_results.append(result)

            logger.info(f'Finished "{analysis_class.analysis_name}"')

        return total_analysis_results
