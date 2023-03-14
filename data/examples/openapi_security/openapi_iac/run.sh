#!/bin/sh

F="data/examples/openapi_security/openapi_iac"
poetry run python -m kube_hound -s -vv -l openapi_iac -c $F "$F/config.yaml"
