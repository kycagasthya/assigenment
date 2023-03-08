docker build --no-cache -t od_train -f train_eval/Dockerfile .
docker tag od_train asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/train-eval:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/train-eval:latest

