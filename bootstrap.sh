#!/bin/bash

export PATH=$PATH:$PY_PATH

set -e

pip3 install virtualenv
pip3 install pipenv

python3 -m virtualenv env

. ./env/bin/activate

pipenv install
