#!/bin/sh

F="data/examples/secrets_in_env"
poetry run python -m kube_hound -vv -l pod_to_pod_traffic -d "$F/config.yaml"
