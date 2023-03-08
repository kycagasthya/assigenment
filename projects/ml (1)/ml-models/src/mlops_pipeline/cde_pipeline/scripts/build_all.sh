# train
docker build --no-cache -t rf_tc -f training/Dockerfile .
docker tag rf_tc asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cde-pipeline/training:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cde-pipeline/training:latest

# eval
docker build --no-cache -t rf_tc -f evaluation/Dockerfile .
docker tag rf_tc asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cde-pipeline/evaluation:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cde-pipeline/evaluation:latest

# updatetoBq
docker build --no-cache -t rf_tc -f updatetobq/Dockerfile .
docker tag rf_tc asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cde-pipeline/updatetobq:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cde-pipeline/updatetobq:latest
