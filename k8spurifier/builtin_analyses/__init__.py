from typing import List, Type
from k8spurifier.analysis import Analysis
from k8spurifier.builtin_analyses.kubesec_analysis import KubesecIntegrationAnalysis
from k8spurifier.builtin_analyses.openapi_securityscheme import SecuritySchemesAnalysis
from k8spurifier.builtin_analyses.secrets_in_env import SecretsInEnvironmentAnalysis

all_analyses: List[Type[Analysis]] = [
    KubesecIntegrationAnalysis,
    SecuritySchemesAnalysis,
    SecretsInEnvironmentAnalysis
]
