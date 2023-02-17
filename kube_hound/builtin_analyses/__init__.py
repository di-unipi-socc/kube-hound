from typing import List, Type
from kube_hound.analysis import Analysis
from kube_hound.builtin_analyses.exposed_services_external_ip import ExposedServicesWithExternalIp
from kube_hound.builtin_analyses.unnecessary_privileges_pods import UnnecessaryPrivilegesToPods
from kube_hound.builtin_analyses.openapi_securityscheme import InsufficientAccessControlOpenAPI
from kube_hound.builtin_analyses.hardcoded_secrets_environment import HardcodedSecretsInEnvironment
from kube_hound.builtin_analyses.unencrypted_pod_to_pod_traffic import UnencryptedPodToPodTraffic

all_analyses: List[Type[Analysis]] = [
    ExposedServicesWithExternalIp,
    UnnecessaryPrivilegesToPods,
    InsufficientAccessControlOpenAPI,
    HardcodedSecretsInEnvironment,
    UnencryptedPodToPodTraffic,
]
