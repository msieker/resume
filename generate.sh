#!/bin/bash

ROOT_DIR=${pwd}

mkdir -p ./output/python
pushd python
source .venv/bin/activate
python3 generate.py --input $ROOT_DIR/data/resume.yaml \
    --template $ROOT_DIR/templates/template.html \
    --output $ROOT_DIR/output/python/resume.html
deactivate
popd