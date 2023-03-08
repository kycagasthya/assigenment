#COPY wheels_v3 wheels_v3
#RUN pip install wheels_v3/wheels/*.whl --ignore-requires-python
FROM asia-south1-docker.pkg.dev/ibank-docai-devops/ibci-docai-docker-ar/cloudbuild/custodbasetraining/mlops:latest
RUN cp -r /home/tensorflow/official /home/tensorflow/models/
WORKDIR /home/tensorflow/models
COPY ./src/mlops_pipeline/custom_od_model_pipeline/components/train_eval/src/ /home/tensorflow/models
ENTRYPOINT ["python", "-m", "/home/tensorflow/models/train_eval.py"]

