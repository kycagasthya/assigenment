docker build -t od_bq -f updatetobq/Dockerfile .
docker tag od_bq asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/updatetobq:latest
docker push asia-south1-docker.pkg.dev/ibank-development/mlops-training-pipeline/custom-od/updatetobq:latest

