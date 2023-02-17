from time import sleep
from typing import List, Mapping
from kube_hound.analysis import AnalysisResult, StaticAnalysis
from loguru import logger
import json
import docker
import requests


from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell


class UnnecessaryPrivilegesToPods(StaticAnalysis):
    analysis_id = 'kubesec_io'
    analysis_name = 'KubeSec analysis'
    analysis_description = 'integration with KubeSec.io analysis tool'
    input_types = ['kubernetes_config']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:
        kubernetes_objects = input_objects.get('kubernetes_config')
        if kubernetes_objects is None:
            return []

        # retrieve the docker client
        self.docker_client = docker.from_env()

        # spawn a kubesec container
        logger.debug('spawning kubesec container')
        kubesec_container = self.docker_client.containers.run(
            'kubesec/kubesec:v2', detach=True, ports={'8080/tcp': 8080})

        output_results = []
        try:
            self.wait_for_running_container(kubesec_container)

            # for each different Kubernetes config, send it to Kubesec
            # and join the results
            seen_paths = set()
            for obj in kubernetes_objects:
                if str(obj.path) in seen_paths:
                    continue
                seen_paths.add(str(obj.path))

                logger.debug(f"processing kubernetes config {obj.path.name}")

                results = self.__process_kubernetes_config(obj)
                output_results += results
        finally:
            # cleanup Kubesec container
            kubesec_container.stop()
            kubesec_container.remove()

        return output_results

    def __process_kubernetes_config(self, obj: ApplicationObject):
        """
        Send the kubernetes config to Kubesec and collect the results
        """

        # read the config file
        with open(obj.path, 'rb') as f:
            raw_data = f.read()

        # send the content to kubesec
        response = requests.post(
            'http://localhost:8080/scan', data=raw_data)

        # parse the results
        data = json.loads(response.text)
        results = []
        for res_obj in data:
            scoring = res_obj.get('scoring')
            if scoring is None:
                continue

            advices = scoring.get('advise')
            if advices is None:
                continue

            # advices contains failed tests, hence smell instances
            for advice in advices:
                description = f"Kubesec.io found potential problems in {obj.path.name}\n" +\
                    f"selector: {advice.get('selector')}\n" +\
                    f"reason: {advice.get('reason')}"

                results.append(
                    AnalysisResult(description, {Smell.UPM}))
        return results

    def wait_for_running_container(self, container):
        """
        Actively wait for a container to become running
        """
        timeout = 120
        stop_time = 0.5
        elapsed_time = 0

        while elapsed_time < timeout:
            sleep(stop_time)
            elapsed_time += stop_time
            container.reload()
            if container.status == 'running':
                return
