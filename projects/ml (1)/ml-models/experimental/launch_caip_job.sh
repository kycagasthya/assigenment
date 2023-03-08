REGION="asia-south1"
JOB_NAME="test_job_$(date '+%Y%m%d_%H%M%S')"
IMAGE_TAG="test-image:v1"
IMAGE_URI="asia.gcr.io/india-dai-parsers/test-containers/${IMAGE_TAG}"
BUCKET="gs://gopalad-sandbox"
MODEL_DIR=$BUCKET/$JOB_NAME

BUILD_IMAGE="false"

if "${BUILD_IMAGE}"; then
  docker build -f Dockerfile -t "${IMAGE_URI}" ./
  docker push "${IMAGE_URI}"
fi


gcloud ai-platform jobs submit training $JOB_NAME \
--master-image-uri $IMAGE_URI \
--region $REGION \
--scale-tier custom \
--master-machine-type=n1-standard-4 \
--master-accelerator=count=1,type=nvidia-tesla-t4 \
-- \
--model_dir $MODEL_DIR \
--epochs 1