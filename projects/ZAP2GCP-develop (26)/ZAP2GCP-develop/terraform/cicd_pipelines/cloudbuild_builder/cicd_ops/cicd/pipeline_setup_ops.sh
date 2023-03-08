#!/bin/bash
set -e
echo "### Activating Python Virtual Environment ###"
source /venv/bin/activate
export c_dir="/workspace"
echo "### Copying Automation Script to /workspace ###"
cp -r /cicd /workspace
cd cicd
echo "### Environment configured for pipeline execution ###"
