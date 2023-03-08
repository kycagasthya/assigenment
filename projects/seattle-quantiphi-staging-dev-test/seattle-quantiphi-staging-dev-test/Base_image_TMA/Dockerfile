FROM gcr.io/ihc-qc-sandbox/dataflow/dev-flex-img-base-image
RUN mkdir -p /dataflow/template
WORKDIR /dataflow/template
# Copy and run the required python modules for the dataflow job
COPY requirements.txt /dataflow/template/requirements.txt
# Install all the packages from requirements.txt
RUN pip install --no-cache-dir -U -r ./requirements.txt
#RUN pip install apache-beam==2.43.0

