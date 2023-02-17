import os
import signal
import subprocess
from time import sleep
from typing import List, Mapping
from kube_hound.analysis import AnalysisResult, DynamicAnalysis
from loguru import logger
from kubernetes import client
import pyshark

from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell

# woarkaround to make pyshark work
import nest_asyncio
nest_asyncio.apply()

MAX_RESULTS_SHOWN = 10
TRAFFIC_MONITORING_TIME = 30  # seconds


class UnencryptedPodToPodTraffic(DynamicAnalysis):
    analysis_id = 'pod_to_pod_traffic'
    analysis_name = 'Traffic analysis'
    analysis_description = 'inspect traffic to detect plaintext requests between services'
    input_types: List[str] = []

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        out_smells = []

        logger.debug('retrieving pod names')

        # get the pod names
        namespace = 'default'
        self.v1 = client.CoreV1Api()
        pods = self.v1.list_namespaced_pod(namespace)
        pod_names = [p.metadata.name for p in pods.items]

        # caputure traffic on the cluster
        out_files = self.__capture_traffic(
            pod_names, namespace, TRAFFIC_MONITORING_TIME)

        # retrieve nodes IPs to filter for healthchecks
        self.nodes_ips = self.__get_nodes_ips()

        for capture, pod_name in zip(out_files, pod_names):
            # try to get HTTP packets
            try:
                http_packets = self.__get_unencrypted_packets(
                    capture, http2=False)
                if len(http_packets) > 0:
                    smell_description = f"Unencrypted traffic detected in pod {pod_name}\n" +\
                        "here is a sample of the packets (HTTP):\n" +\
                        '\n'.join(http_packets)
                    out_smells.append(AnalysisResult(
                        smell_description, {Smell.NSC}))
                    continue
            except:
                pass

            # try to get HTTP2 packets
            try:
                http2_packets = self.__get_unencrypted_packets(
                    capture, http2=True)
                if len(http2_packets) > 0:
                    smell_description = f"Unencrypted traffic detected in pod {pod_name}\n" +\
                        "here is a sample of the packets (HTTP2, maybe gRPC?):\n" +\
                        '\n'.join(http2_packets)
                    out_smells.append(AnalysisResult(
                        smell_description, {Smell.NSC}))
                    continue
            except:
                pass

        return out_smells

    def __get_unencrypted_packets(self, capture, http2: bool) -> List[str]:
        """
        Get a sample of unencrypted packets in a given capture file, if any exists.
        If http2 is set, the capture file is set to be decoded on all ports as HTTP2
        """
        if not http2:
            cap = pyshark.FileCapture(capture)
        else:
            cap = pyshark.FileCapture(
                capture, decode_as={'tcp.port==0-65536': 'http2'})

        count = 0
        out_packets = []
        for packet in cap:
            if count > MAX_RESULTS_SHOWN:
                break

            # consider only IP packets
            if 'IP' not in packet:
                continue

            # filter healthchecks
            if packet.ip.src in self.nodes_ips or packet.ip.dst in self.nodes_ips:
                continue

            if 'HTTP' in packet:
                hex_payload = packet.tcp.payload
                payload = bytes([int(x, 16)
                                for x in hex_payload.split(':')])
                first_line = payload.split(b'\n')[0].split(b'\r')[0]

                try:
                    first_line_decoded = first_line.decode()

                except:
                    # tshark will create a false positive HTTP layer also on encrypted packets
                    # as an euristic, we assume that if we cannot decode the bytes as plaintext,
                    # then it is encrypted
                    continue

                description = f"HTTP {packet.ip.src} -> {packet.ip.dst} : {first_line_decoded}"
                out_packets.append(description)
                count += 1

            if 'HTTP2' in packet:
                # filter out false positives (empty HTTP2 layer)
                if not packet.http2.has_field('length'):
                    continue

                description = f"HTTP2 {packet.ip.src} -> {packet.ip.dst}"
                out_packets.append(description)
                count += 1
        return out_packets

    def __capture_traffic(self, pod_names, namespace, timeout) -> List[str]:
        """
        Capture traffic on the cluster for timeout seconds
        """
        logger.debug('spawning ksniff pods')

        # spawn the Ksniff instances
        processes = []
        out_files = []
        for pod in pod_names:
            process, out_file = self.__spawn_traffic_container(pod, namespace)
            processes.append(process)
            out_files.append(out_file)

        # only record for timeout seconds
        sleep(timeout)
        for p in processes:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)

        # cleanup ksniff pods
        logger.debug('cleaning up ksniff pods')
        pods = self.v1.list_namespaced_pod(namespace)
        for pod in pods.items:
            app = pod.metadata.labels.get('app')
            if app == 'ksniff':
                logger.debug(f'deleting pod {pod.metadata.name}')
                self.v1.delete_namespaced_pod(
                    pod.metadata.name, pod.metadata.namespace)

        return out_files

    def __spawn_traffic_container(self, pod_name: str, namespace: str):
        """
        Spawn a Ksniff instance for a specific pod
        """
        logger.debug(f'spawning snffer for {pod_name}')
        filename = f'/tmp/{pod_name}.pcap'
        cmd = f"kubectl sniff -p -v -i eth0 -n {namespace} -o {filename} {pod_name}"
        logger.debug('command:', cmd)
        return subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE,
                                # stderr=subprocess.DEVNULL,
                                preexec_fn=os.setsid), filename

    def __get_nodes_ips(self) -> List[str]:
        """
        Get the IPs of all worker nodes
        """
        nodes = self.v1.list_node()
        out_ips = []
        for node in nodes.items:
            addresses = node.status.addresses
            out_ips += [x.address
                        for x in addresses if x.type == 'ExternalIP']
        return out_ips
