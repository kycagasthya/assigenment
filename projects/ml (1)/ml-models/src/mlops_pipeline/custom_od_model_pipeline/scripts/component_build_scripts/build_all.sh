docker build -t od_eval -f evaluation/Dockerfile .
docker tag od_eval asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/evaluation:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/evaluation:latest

docker build --no-cache -t od_export -f export_model/Dockerfile .
docker tag od_export asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/model-export:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/model-export:latest

docker build -t od_pre -f preprocess/Dockerfile .
docker tag od_pre asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/preprocessing:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/preprocessing:latest

docker build -t od_train -f train_eval/Dockerfile .
docker tag od_train asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/train-eval:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/train-eval:latest

docker build -t od_bq -f updatetobq/Dockerfile .
docker tag od_bq asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/updatetobq:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/updatetobq:latest