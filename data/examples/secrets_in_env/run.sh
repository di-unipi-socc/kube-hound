#!/bin/sh

F="data/examples/secrets_in_env"
poetry run python -m kube_hound -vv -l secrets_in_env -d "$F/config.yaml"
