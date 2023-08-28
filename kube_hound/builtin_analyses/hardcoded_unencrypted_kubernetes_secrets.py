from typing import List, Mapping
import logging

from kube_hound.analysis import AnalysisResult, StaticAnalysis
from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell

from checkov.runner_filter import RunnerFilter
from checkov.secrets.runner import Runner as SecretRunner


class HardcodedSecretsInKubernetes(StaticAnalysis):
    analysis_id = 'kubernetes_secrets'
    analysis_name = 'Unencryped kubernetes secrets analysis'
    analysis_description = 'Detect harcoded unencrypted secrets in kubernetes'
    input_types = ['kubernetes_config']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        # logging.getLogger().setLevel(logging.CRITICAL) # Not showing checkov logger

        kubernetes_objects = input_objects.get('kubernetes_config')
        if kubernetes_objects is None:
            return []

        results = []
        for document in kubernetes_objects:
            document_content = document.get_content()
            if document_content['kind'] == 'Secret':
                results.extend(self.__check_kubernetes_secret(document))

        return results

    def __check_kubernetes_secret(self, secret: ApplicationObject) -> List[AnalysisResult]:
        report = SecretRunner().run(
            root_folder=None,
            files=[str(secret.path)],
            runner_filter=RunnerFilter(show_progress_bar=False)
        )

        secret_fail_response = []
        if not report.is_empty():  # Check for failures
            failed_checks = report.failed_checks  # Get failures
            for fail in failed_checks:
                fail_found_desc = ''
                match fail.check_id:
                    case 'CKV_SECRET_6':
                        fail_found_desc = 'Base64 High Entropy String'

                    case 'CKV_SECRET_19':
                        fail_found_desc = 'Hex High Entropy'

                    case _:
                        continue

                blocks = []
                for code_block in fail.code_block:  # Take the blocks of code that generated the failure
                    blocks.append(
                        str(code_block[0]) + ' |' + code_block[1]
                    )

                description = f'Description: {fail_found_desc}\n' +\
                    f'File: {fail.file_path}:{str(fail.file_line_range[0])}-{str(fail.file_line_range[1])} \n' +\
                    'Error(s): \n' +\
                    '\n'.join('-- ' + block for block in blocks)

                secret_fail_response.append(
                    AnalysisResult(description, {Smell.HS})
                )

        return secret_fail_response
