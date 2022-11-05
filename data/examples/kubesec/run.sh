#!/bin/sh

F="data/examples/kubesec"
poetry run python -m kube_hound -s -l kubesec_io -v -c $F "$F/config.yaml"
