import json
import logging
import os
import tarfile

from datetime import datetime
from google.cloud import storage
from google.cloud.devtools import cloudbuild_v1


timestamp = datetime.now()
filename = timestamp.strftime("%m%d%Y-%H%M%S")
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO)


class DataflowTemplate():
    def __init__(self, working_dir: str, project: str):
        self.working_dir = working_dir
        self.project = project

    def _create_tarball(self) -> str:
        with tarfile.open(f"{self.working_dir}/{filename}.tgz", "w:gz") as tgz:
            os.chdir(f"{self.working_dir}/dataflow/template")
            tgz.add(".")
            os.chdir(self.working_dir)

        return f"{self.working_dir}/{filename}.tgz"

    def _upload_blob(self, source_object: str, destination: str) -> tuple[str, str]:
        """Uploads a file to the bucket."""

        filename = os.path.basename(source_object)
        storage_bucket = destination.split("/", 1)[0]
        if len(destination.split("/", 1)) == 1:
            object_path = ""
        else:
            object_path = destination.split("/", 1)[1]

        storage_client = storage.Client()
        bucket = storage_client.bucket(storage_bucket)
        blob = bucket.blob(f"{object_path}/{filename}")

        blob.upload_from_filename(source_object)
        logging.info(f"File {source_object} uploaded to {destination}")
        os.remove(source_object)

        return storage_bucket, str(blob.name)

    def _submit_build(self, source_bucket: str, source_object: str) -> bool:
        """Create and execute a simple Google Cloud Build configuration,
        print the in-progress status and print the completed status."""

        # Authorize the client with Google defaults
        # credentials, project_id = google.auth.default()
        client = cloudbuild_v1.services.cloud_build.CloudBuildClient()
        build = cloudbuild_v1.Build()

        build.steps = [
            {
                "name": "gcr.io/cloud-builders/docker",
                "args": [
                    "build",
                    "--no-cache",
                    "-t",
                    f"gcr.io/{self.project}/test-py-image:latest",
                    "."
                ]
            },
            {
                "name": "gcr.io/cloud-builders/docker",
                "args": [
                    "push",
                    f"gcr.io/{self.project}/test-py-image:latest"
                ]
            }
        ]

        build.source = {
            "storage_source": {
                "bucket": source_bucket,
                "object_": source_object
            }
        }

        operation = client.create_build(project_id=self.project, build=build)
        logging.info(f"The build has been submitted...")
        print("IN PROGRESS:")
        print(operation.metadata)

        result = operation.result()
        print("RESULT:", result.status)

        return True if str(result.status) == "Status.SUCCESS" else False

    def _create_template(self) -> str:
        config = {
            "defaultEnvironment": {},
            "image": f"gcr.io/{self.project}/test-py-image:latest",
            "sdkInfo": {
                "language": "PYTHON"
            }
        }
        with open(f"{self.working_dir}/test-py-image-latest.json", 'w') as file_handler:
            json.dump(config, file_handler)

        return f"{self.working_dir}/test-py-image-latest.json"

    def create(self) -> str:
        bucket, blob = self._upload_blob(
            source_object=self._create_tarball(),
            destination=f"{self.project}-service/tarballs"
        )
        if self._submit_build(source_bucket=bucket, source_object=blob):
            tpl_bucket, tpl_blob = self._upload_blob(
                source_object=self._create_template(),
                destination=f"{self.project}-artifacts/templates"
            )
        else:
            raise RuntimeError(
                "Something went wrong while building template image.")

        return f"gs://{tpl_bucket}/{tpl_blob}"
