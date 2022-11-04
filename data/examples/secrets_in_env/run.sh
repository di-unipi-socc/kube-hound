#!/bin/sh

F="data/examples/secrets_in_env"
poetry run python -m k8spurifier -vv -l secrets_in_env -d "$F/config.yaml"
