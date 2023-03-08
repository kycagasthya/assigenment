docker build -t rf_tc -f evaluation/Dockerfile .
docker tag rf_tc asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cde-pipeline/evaluation:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/cde-pipeline/evaluation:latest

