FROM asia-south1-docker.pkg.dev/ibank-docai-devops/ibci-docai-docker-ar/cloudbuild/custod/mlops:latest
WORKDIR /app

#COPY ./cdc_pipeline/scripts/requirements.txt  cdc_pipeline/scripts/requirements.txt 
COPY ./src/mlops_pipeline/custom_od_model_pipeline/scripts/component_build_scripts/requirements_common.txt requirements.txt 

RUN pip install -r requirements.txt   --extra-index-url https://asia-south1-python.pkg.dev/ibank-docai-devops/ibci-docai-python-ar/simple

COPY ./src/mlops_pipeline/custom_od_model_pipeline/components/updatetobq/src/ .

ENTRYPOINT ["python", "-m", "/app/update_to_bq_od.py"]
