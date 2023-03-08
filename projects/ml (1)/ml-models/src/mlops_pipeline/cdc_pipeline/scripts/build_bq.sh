docker build -t rf_tc -f updatetobq/Dockerfile .
docker tag rf_tc asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/updatetobq:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/updatetobq:latest
