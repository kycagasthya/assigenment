FROM asia-south1-docker.pkg.dev/ibank-docai-devops/ibci-docai-docker-ar/cloudbuild/custodbase/mlops:latest
#WORKDIR /app
COPY ./src/mlops_pipeline/custom_od_model_pipeline/components/export_model/src/export_model.py /home/tensorflow/models/
COPY ./src/mlops_pipeline/custom_od_model_pipeline/components/export_model/src/custlogger.py /home/tensorflow/models/
#COPY ./cdc_pipeline/scripts/requirements.txt  cdc_pipeline/scripts/requirements.txt 
COPY ./src/mlops_pipeline/custom_od_model_pipeline/scripts/component_build_scripts/requirements_export.txt requirements.txt 
RUN pip install -r requirements.txt  --extra-index-url https://asia-south1-python.pkg.dev/ibank-docai-devops/ibci-docai-mlopsod-ar
#COPY ./src/mlops_pipeline/custom_od_model_pipeline/components/export_model/src/ .
RUN cp -r /home/tensorflow/official /home/tensorflow/models/
#COPY /home/tensorflow/official /home/tensorflow/models/ 
#ENTRYPOINT ["python", "-m", "/home/tensorflow/models/"]

ENTRYPOINT ["python", "-m", "/home/tensorflow/models/export_model.py", "/home/tensorflow/models/custlogger.py"]