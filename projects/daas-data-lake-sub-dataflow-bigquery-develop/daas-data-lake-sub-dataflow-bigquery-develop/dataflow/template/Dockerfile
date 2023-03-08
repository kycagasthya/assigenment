# Dataflow flex template image
FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG WORKDIR=/dataflow/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

COPY ingest_job_main.py .
COPY setup.py .
ADD takeoff ./takeoff

ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/ingest_job_main.py"

# Install apache-beam and other dependencies to launch the pipeline
RUN pip install apache-beam[gcp]==2.41.0
RUN pip install .