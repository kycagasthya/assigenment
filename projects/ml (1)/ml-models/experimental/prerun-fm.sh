#!/bin/bash
echo "______________________UNINSTALLING EXISTING PACKAGE - docai-fuzzymatch______________________"
pip uninstall -y docai-fuzzymatch
echo "______________________BUILDING NEW PACKAGE - docai-fuzzymatch______________________"
cd ../src/docai-fuzzymatch
rm -rf ./dist/*
python setup.py sdist bdist_wheel
echo "______________________INSTALLING NEW PACKAGE - docai-fuzzymatch______________________"
cd ./dist
pip install *.whl