docker build -t rf_tc -f training/Dockerfile .
docker tag rf_tc asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/training:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/training:latest
