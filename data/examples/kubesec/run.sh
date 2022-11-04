#!/bin/sh

F="data/examples/kubesec"
poetry run python -m k8spurifier -s -l kubesec_io -v -c $F "$F/config.yaml"
