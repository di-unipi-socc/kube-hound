from typing import Dict, List, Mapping
from k8spurifier.analysis import AnalysisResult, StaticAnalysis
from loguru import logger
import subprocess
import json
import docker
import requests


from k8spurifier.applicationobject import ApplicationObject
from k8spurifier.smells import Smell


class KubesecIntegrationAnalysis(StaticAnalysis):
    analysis_id = 'S0'
    analysis_name = 'KubeSec analysis'
    analysis_description = 'integration with KubeSec.io analysis tool'
    input_types = ['kubernetes_config']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) -> List[AnalysisResult]:
        kubernetes_objects = input_objects.get('kubernetes_config')

        docker_client = docker.from_env()

        # spawn kubesec container
        logger.debug('spawning kubesec container')
        kubesec_container = docker_client.containers.run(
            'kubesec/kubesec:v2', detach=True, ports={'8080/tcp': 8080})

        try:
            seen_paths = set()
            output_results = []
            for obj in kubernetes_objects:
                if str(obj.path) in seen_paths:
                    continue
                seen_paths.add(str(obj.path))

                logger.debug(f"processing kubernetes config {obj.path.name}")

                results = self.process_kubernetes_config(obj)
                output_results += results
        finally:
            kubesec_container.stop()
            kubesec_container.remove()

        return output_results

    def process_kubernetes_config(self, obj: ApplicationObject):
        with open(obj.path, 'rb') as f:
            raw_data = f.read()
        response = requests.post(
            'http://localhost:8080/scan', data=raw_data)

        data = json.loads(response.text)

        results = []
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

                results.append(
                    AnalysisResult(description, {Smell.UPM}))
        return results
