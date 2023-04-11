#!/bin/sh

F="data/examples/secrets_kubernetes"
poetry run python -m kube_hound -s -l kubernetes_secrets -v -c $F "$F/config.yaml"