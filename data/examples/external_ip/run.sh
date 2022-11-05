#!/bin/sh

F="data/examples/external_ip"
poetry run python -m kube_hound -vv -l external_ip -c "$F" -d "$F/config.yaml"
