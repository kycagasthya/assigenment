docker build -t od_eval -f evaluation/Dockerfile .
docker tag od_eval asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/evaluation:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/evaluation:latest

