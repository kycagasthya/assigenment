#!/bin/bash
echo "______________________UNINSTALLING EXISTING PACKAGE - docai-processor______________________"
pip uninstall -y docai-processor
echo "______________________BUILDING NEW PACKAGE - docai-processor______________________"
cd ~/api/ml-models/src/docai-processor
python setup.py sdist bdist_wheel
echo "______________________INSTALLING NEW PACKAGE - docai-processor______________________"
cd ~/api/ml-models/src/docai-processor/dist
pip install docai_processor-1.0.3-py3-none-any.whl