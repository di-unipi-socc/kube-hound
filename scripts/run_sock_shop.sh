#!/bin/sh
poetry run python -m kube_hound -vv -s -c test_files/sock-shop/application test_files/sock-shop/sock-shop-config.yaml