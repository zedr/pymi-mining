#!/usr/bin/env bash

set -o pipefail
set -o errexit
set -o nounset

ruff check . --fix
pyright .
black .
