#!/bin/sh

F="data/examples/dbms_rest_enc"
poetry run python -m kube_hound -s -l dbms_rest_encryption -v -vv -c $F "$F/config.yaml"