#!/usr/bin/env bash

set -o pipefail
set -o errexit
set -o nounset

echo "... Running ruff ..."
ruff check . --fix
echo "... Running pyright ..."
pyright irc_client.py
echo "... Running black ..."
black .
