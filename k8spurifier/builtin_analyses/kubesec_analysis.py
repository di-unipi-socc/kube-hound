from typing import Dict, List, Mapping
from k8spurifier.analysis import AnalysisResult, StaticAnalysis
from loguru import logger
import subprocess
import json


from k8spurifier.applicationobject import ApplicationObject
from k8spurifier.smells import Smell


class KubesecIntegrationAnalysis(StaticAnalysis):
    analysis_id = 'S0'
    analysis_name = 'KubeSec analysis'
    analysis_description = 'integration with KubeSec.io analysis tool'
    input_types = ['kubernetes_config']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) -> List[AnalysisResult]:
        kubernetes_objects = input_objects.get('kubernetes_config')

        seen_paths = set()
        output_results = []
        for obj in kubernetes_objects:
            if str(obj.path) in seen_paths:
                continue
            seen_paths.add(str(obj.path))

            logger.debug(f"processing kubernetes config {obj.path.name}")

            command = f'docker run -i kubesec/kubesec:v2 scan /dev/stdin < {obj.path}'
            result = subprocess.run(command, shell=True, capture_output=True)
            response = result.stdout.decode()

            data = json.loads(response)

            for res_obj in data:
                scoring = res_obj.get('scoring')
                if scoring is None:
                    continue

                advices = scoring.get('advise')
                if advices is None:
                    continue

                for advice in advices:
                    description = f"Kubesec.io found potential problems in {obj.path.name}\n" +\
                        f"selector: {advice.get('selector')}\n" +\
                        f"reason: {advice.get('reason')}"

                    output_results.append(
                        AnalysisResult(description, {Smell.UPM}))

        return output_results
