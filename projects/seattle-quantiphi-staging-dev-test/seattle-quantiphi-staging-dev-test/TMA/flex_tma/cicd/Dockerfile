FROM gcr.io/ihc-qc-sandbox/dataflow/dev-tma-flex-img4-base-image
# FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

# RUN mkdir -p /dataflow/template
# WORKDIR /dataflow/template

# # Copy and run the required python modules for the dataflow job
# COPY requirements.txt /dataflow/template/requirements.txt

# # Install all the packages from requirements.txt
# RUN pip install --no-cache-dir -U -r ./requirements.txt

# # Additional installations

# # Old apt-get update command 
# RUN apt-get update

# # New apt-get comment added on 21-02-2022
# # RUN apt-get update && apt-get install -y apt-transport-https

# RUN apt-get --assume-yes install openslide-tools
# # RUN apt-get --assume-yes install python-openslide
# RUN pip install --no-cache-dir -U openslide-python
# RUN apt-get install -y python3-openslide
# # RUN apt-get install -y python-openslide

# RUN pip install opencv-python
# RUN apt-get install libgl1-mesa-glx -y


# RUN pip install tifffile

# Copy the files into the Image
COPY . .

# Entry point for the Dataflow job.
# By setting this variable, no need for setting 
#ENV DATAFLOW_PYTHON_COMMAND_SPEC="/dataflow/template/metadata.json"

ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/dataflow/template/script.py"
