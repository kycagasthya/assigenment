#!/bin/bash
echo "______________________UNINSTALLING EXISTING PACKAGE - docai-processor______________________"
pip uninstall -y docai-docsplit
echo "______________________BUILDING NEW PACKAGE - docai-processor______________________"
cd ../src/docai-docsplit
rm -rf ./dist/*
python setup.py sdist bdist_wheel
echo "______________________INSTALLING NEW PACKAGE - docai-processor______________________"
cd ./dist
pip install *.whl
