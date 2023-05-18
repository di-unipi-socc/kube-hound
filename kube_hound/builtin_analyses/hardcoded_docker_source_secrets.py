from typing import List, Mapping
from loguru import logger

from kube_hound.analysis import AnalysisResult, StaticAnalysis
from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell

from checkov.runner_filter import RunnerFilter
from checkov.secrets.runner import Runner as SecretRunner
from checkov.secrets.runner import SOURCE_CODE_EXTENSION


class HardcodedSecretsInDockerAndSource(StaticAnalysis):
    analysis_id = 'docker_source_secrets'
    analysis_name = 'Hardcoded docker and source secrets analysis'
    analysis_description = 'Detect harcoded secrets in docker and source code'
    input_types = ['dockerfile', 'sourcecode']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        # logging.getLogger().setLevel(logging.CRITICAL) # Not showing checkov logger

        docker_object = input_objects.get('dockerfile')
        source_object = input_objects.get('sourcecode')

        results = []
        if docker_object is None and source_object is None:
            return results
        else:
            if docker_object is not None:
                results.extend(self.__iterate_input(docker_object))

            if source_object is not None:
                logger.info('Supported file extensions for source code: ' + ' '.join(SOURCE_CODE_EXTENSION))
                results.extend(self.__iterate_input(source_object))

        return results

    def __iterate_input(self, input_list: List[ApplicationObject]) -> List[AnalysisResult]:
        results = []
        for input_obj in input_list:
            results.extend(self.__check_secrets(input_obj))

        return results

    def __check_secrets(self, input_obj: ApplicationObject) -> List[AnalysisResult]:
        report = None
        if input_obj.type == 'sourcecode':
            report = SecretRunner().run(
                root_folder=str(input_obj.path),
                runner_filter=RunnerFilter(
                    show_progress_bar=False,
                    enable_secret_scan_all_files=True
                )
            )
        elif input_obj.type == 'dockerfile':
            report = SecretRunner().run(
                root_folder=None,
                files=[str(input_obj.path)],
                runner_filter=RunnerFilter(show_progress_bar=False)
            )
        else:
            raise ValueError("The object type isn't supported")

        secret_fail_response = []
        if not report.is_empty(): # Check for failures
            failed_checks = report.failed_checks # Get failures
            for fail in failed_checks:
                blocks = []

                for code_block in fail.code_block: # Take the blocks of code that generated the failure
                    blocks.append(
                        str(code_block[0]) + ' |' + code_block[1]
                    )

                description = f'Description: {fail.check_name}\n' +\
                    f'File: {fail.file_path}:{str(fail.file_line_range[0])}-{str(fail.file_line_range[1])} \n' +\
                    'Error(s): \n' +\
                    '\n'.join('-- ' + block for block in blocks)

                secret_fail_response.append(
                    AnalysisResult(description, {Smell.HS})
                )

        return secret_fail_response
