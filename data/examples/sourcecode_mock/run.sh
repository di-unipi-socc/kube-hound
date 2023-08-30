#!/bin/sh

F="data/examples/sourcecode_mock"
poetry run python -m kube_hound -vv -s "$F/config.yaml"
