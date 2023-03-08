FROM asia-south1-docker.pkg.dev/ibank-docai-devops/ibci-docai-docker-ar/cloudbuild/mlops:latest

WORKDIR /app

#COPY ./cdc_pipeline/scripts/requirements.txt  cdc_pipeline/scripts/requirements.txt 
COPY ./src/mlops_pipeline/cde_pipeline/scripts/requirements.txt .

RUN pip install -r requirements.txt --extra-index-url https://asia-south1-python.pkg.dev/ibank-docai-devops/ibci-docai-python-ar/simple

COPY ./src/mlops_pipeline/cde_pipeline/components/training/src/ .
#update entrypoint
ENTRYPOINT ["python", "-m", "/app/training_cde.py"]


