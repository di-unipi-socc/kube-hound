import os
import signal
import subprocess
import multiprocessing
from time import sleep
from typing import List, Mapping
from k8spurifier.analysis import AnalysisResult, DynamicAnalysis, StaticAnalysis
from loguru import logger
from kubernetes import client
import pyshark

from k8spurifier.applicationobject import ApplicationObject

# woarkaround to make pyshark work
import nest_asyncio

from k8spurifier.smells import Smell
nest_asyncio.apply()

MAX_RESULTS_SHOWN = 10
TRAFFIC_MONITORING_TIME = 30  # seconds


class TrafficAnalysis(DynamicAnalysis):
    analysis_id = 'D1'
    analysis_name = 'Traffic analysis'
    analysis_description = 'inspect traffic to detect plaintext requests between services'
    input_types = []

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        out_smells = []

        logger.debug('retrieving pod names')
        self.v1 = client.CoreV1Api()
        pods = self.v1.list_namespaced_pod('default')
        pod_names = [p.metadata.name for p in pods.items]

        out_files = self.__capture_traffic(
            pod_names, TRAFFIC_MONITORING_TIME)

        nodes_ips = self.__get_nodes_ips()

        for capture, pod_name in zip(out_files, pod_names):
            cap = pyshark.FileCapture(capture)
            count = 0
            out_packets = []
            for packet in cap:
                if 'HTTP' in packet:
                    if count > MAX_RESULTS_SHOWN:
                        break

                    # filter healthchecks
                    if packet.ip.src in nodes_ips or packet.ip.dst in nodes_ips:
                        continue

                    hex_payload = packet.tcp.payload
                    payload = bytes([int(x, 16)
                                    for x in hex_payload.split(':')])
                    first_line = payload.split(b'\r\n')[0]

                    description = f"HTTP {packet.ip.src} -> {packet.ip.dst} : {first_line.decode()}"
                    out_packets.append(description)
                    count += 1

            if count > 0:
                smell_description = f"Unencrypted traffic detected in pod {pod_name}\n" +\
                    f"here are the first {MAX_RESULTS_SHOWN} packets:\n" +\
                    '\n'.join(out_packets)
                out_smells.append(AnalysisResult(
                    smell_description, {Smell.NSC}))

        return out_smells

    def __capture_traffic(self, pod_names, timeout):
        logger.debug('spawning ksniff pods')
        processes = []
        out_files = []
        for pod in pod_names:
            process, out_file = self.__spawn_traffic_container(pod)
            processes.append(process)
            out_files.append(out_file)

        sleep(timeout)
        for p in processes:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)

        # cleanup ksniff pods
        logger.debug('cleaning up ksniff pods')
        pods = self.v1.list_namespaced_pod('default')
        for pod in pods.items:
            app = pod.metadata.labels.get('app')
            if app == 'ksniff':
                logger.debug(f'deleting pod {pod.metadata.name}')
                self.v1.delete_namespaced_pod(
                    pod.metadata.name, pod.metadata.namespace)

        return out_files

    def __spawn_traffic_container(self, pod_name: str):
        logger.debug(f'spawning snffer for {pod_name}')
        filename = f'/tmp/{pod_name}.pcap'
        cmd = f"kubectl sniff -p -v -i eth0 -o {filename} {pod_name}"
        logger.debug('command:', cmd)
        return subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE,
                                # stderr=subprocess.DEVNULL,
                                preexec_fn=os.setsid), filename

    def __get_nodes_ips(self):
        nodes = self.v1.list_node()
        out_ips = []
        for node in nodes.items:
            addresses = node.status.addresses
            out_ips += [x.address
                        for x in addresses if x.type == 'ExternalIP']
        return out_ips
