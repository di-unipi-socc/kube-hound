#!/bin/sh

F="data/examples/sourcecode_ucp"
poetry run python -m kube_hound -vv -s "$F/config.yaml"
