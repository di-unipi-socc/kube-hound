#!/bin/sh
echo "========== Runnning Mypy =========="
poetry run python -m mypy --ignore-missing-imports --exclude test_files . 
echo "========= Runnning flake8 ========="
poetry run python -m flake8 --max-line-length=100 --exclude test_files
