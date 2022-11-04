#!/bin/sh

F="data/examples/openapi_security"
poetry run python -m k8spurifier -s -v -l openapi_securityscheme -c $F "$F/config.yaml"
