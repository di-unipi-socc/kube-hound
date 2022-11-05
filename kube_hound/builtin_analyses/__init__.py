from typing import List, Type
from kube_hound.analysis import Analysis
from kube_hound.builtin_analyses.externalip_analysis import ExternalIpAnalysis
from kube_hound.builtin_analyses.kubesec_analysis import KubesecIntegrationAnalysis
from kube_hound.builtin_analyses.openapi_securityscheme import SecuritySchemesAnalysis
from kube_hound.builtin_analyses.secrets_in_env import SecretsInEnvironmentAnalysis
from kube_hound.builtin_analyses.traffic_analysis import TrafficAnalysis

all_analyses: List[Type[Analysis]] = [
    ExternalIpAnalysis,
    KubesecIntegrationAnalysis,
    SecuritySchemesAnalysis,
    SecretsInEnvironmentAnalysis,
    TrafficAnalysis,
]
