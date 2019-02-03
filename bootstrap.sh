#!/bin/bash

export PATH=$PATH:$PY_PATH

set -e

python3 -m virtualenv env

. ./env/bin/activate

pipenv install
