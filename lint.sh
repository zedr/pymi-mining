#!/usr/bin/env bash

set -o pipefail
set -o errexit
set -o nounset

echo "... Running ruff ..."
ruff check . --fix
echo "... Running pyright ..."
pyright .
echo "... Running black ..."
black .
