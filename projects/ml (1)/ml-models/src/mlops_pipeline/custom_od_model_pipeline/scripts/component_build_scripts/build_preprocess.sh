docker build --no-cache -t od_pre -f preprocess/Dockerfile .
docker tag od_pre asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/preprocessing:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/preprocessing:latest

