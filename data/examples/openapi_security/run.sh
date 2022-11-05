#!/bin/sh

F="data/examples/openapi_security"
poetry run python -m kube_hound -s -v -l openapi_securityscheme -c $F "$F/config.yaml"
