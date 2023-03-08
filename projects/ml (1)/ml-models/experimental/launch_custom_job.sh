REGION="asia-south1"
JOB_NAME="test_job_$(date '+%Y%m%d_%H%M%S')"
IMAGE_TAG="test-image:v1"
BUCKET="gs://gopalad-sandbox"
MODEL_DIR=$BUCKET/$JOB_NAME
IMAGE_URI="asia-south1-docker.pkg.dev/india-dai-parsers/test-containers/${IMAGE_TAG}"

BUILD_IMAGE="false"

if "${BUILD_IMAGE}"; then
  docker build -f Dockerfile -t "${IMAGE_URI}" ./
  docker push "${IMAGE_URI}"
fi


gcloud ai custom-jobs create \
--region=$REGION \
--display-name=$JOB_NAME \
--worker-pool-spec=machine-type=n1-standard-4,accelerator-type=NVIDIA_TESLA_T4,container-image-uri=$IMAGE_URI \
--args=--epochs,1,--model_dir,$MODEL_DIR
