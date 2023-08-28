from typing import List, Mapping

from kube_hound.analysis import AnalysisResult, StaticAnalysis
from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell

from checkov.runner_filter import RunnerFilter
from checkov.terraform.runner import Runner as TFRunner

SUPPORTED_DBMS_POLICIES = [
    'CKV_ALI_22',
    'CKV_ALI_44',
    'CKV2_AZURE_25',
    'CKV_AZURE_96',
    'CKV_AZURE_130',
    'CKV_AWS_5',
    'CKV_AWS_16',
    'CKV_AWS_74',
    'CKV_AWS_77',
    'CKV_AWS_201',
]


class DBMSDataAtRestEncryption(StaticAnalysis):
    analysis_id = 'dbms_rest_encryption'
    analysis_name = 'Data-at-Rest Encryption Not Enabled in DBMSs'
    analysis_description = 'detect whether encryption-at-rest of data is enabled in database management systems'
    input_types: List[str] = ['terraform']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        terraform_objects = input_objects.get('terraform')
        if terraform_objects is None:
            return []

        results = []
        for document in terraform_objects:
            results.extend(self.__check_terraform_file(document))

        return results

    def __check_terraform_file(self, document: ApplicationObject) -> List[AnalysisResult]:
        report = TFRunner().run(
            root_folder=None,
            files=[str(document.path)],
            runner_filter=RunnerFilter(show_progress_bar=False)
        )

        secret_fail_response = []
        if not report.is_empty():  # Check for failures
            failed_checks = report.failed_checks  # Get failures
            for fail in failed_checks:

                if fail.check_id in SUPPORTED_DBMS_POLICIES:
                    description = f'Description: {fail.check_name} \n' +\
                        f'File type: {document.type} \n' +\
                        f'File: {fail.file_path}:{str(fail.file_line_range[0])}-{str(fail.file_line_range[1])}'

                    secret_fail_response.append(
                        AnalysisResult(description, {Smell.NEDE})
                    )

        return secret_fail_response