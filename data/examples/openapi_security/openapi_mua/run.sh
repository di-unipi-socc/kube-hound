#!/bin/sh

F="data/examples/openapi_security/openapi_mua"
poetry run python -m kube_hound -s -vv -l openapi_mua -c $F "$F/config.yaml"
