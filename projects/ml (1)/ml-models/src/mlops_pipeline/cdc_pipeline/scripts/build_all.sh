docker build --no-cache -t rf_tc -f updatetobq/Dockerfile .
docker tag rf_tc asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/updatetobq:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/updatetobq:latest
docker build --no-cache -t rf_tc -f evaluation/Dockerfile .
docker tag rf_tc asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/evaluation:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/evaluation:latest
docker build --no-cache -t rf_tc -f training/Dockerfile .
docker tag rf_tc asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/training:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cdc-pipeline/training:latest
