#!/bin/sh

F="data/examples/secrets_in_docker_source"
poetry run python -m kube_hound -s -l docker_source_secrets -v -vv -c $F "$F/config.yaml"