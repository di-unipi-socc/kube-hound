import os
import pathlib

from typing import List, Mapping
from loguru import logger
import logging

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

        docker_objects = input_objects.get('dockerfile')        
        source_objects = input_objects.get('sourcecode')

        results = []
        if docker_objects is None and source_objects is None:
            return result
        else: 
            if docker_objects is not None:
                results.extend(self.__iterate_input(docker_objects))
            
            if source_objects is not None:
                logger.info('Hardcoded secret - supported file extensions for source code: ' + ' '.join(SOURCE_CODE_EXTENSION))
                results.extend(self.__iterate_input(source_objects))
        
        return results

    def __iterate_input(self, input_list: List[ApplicationObject]) -> List[AnalysisResult]:
        results = []
        for input_obj in input_list:
            if input_obj.type == 'sourcecode' and os.path.isdir(input_obj.path):
                files = self.__get_source_files(input_obj.path)
                input_list.extend(files)

            results.extend(self.__check_secrets(input_obj))
            
        return results
    
    def __get_source_files(self, folder_path: str) -> List[ApplicationObject]:
        files = []
        for file in pathlib.Path(folder_path).rglob("*.*"):
            if file.is_file():
                files.append(ApplicationObject('sourcecode', file, None))
        
        return files

    def __check_secrets(self, input_file: ApplicationObject) -> List[AnalysisResult]:
        report = SecretRunner().run(
            root_folder=None, files=[str(input_file.path)], runner_filter=RunnerFilter(show_progress_bar=False)
        )

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
                    f'File type: ' + input_file.type + '\n' +\
                    f'File: ' + fail.file_path + ':' + str(fail.file_line_range[0]) + '-' + str(fail.file_line_range[1]) + '\n' +\
                    f'Error(s):\n' +\
                    f'\n'.join('-- ' + block for block in blocks)
                
                secret_fail_response.append(
                    AnalysisResult(description, {Smell.HS})
                )
        
        return secret_fail_response