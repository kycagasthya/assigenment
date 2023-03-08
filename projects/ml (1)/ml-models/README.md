# Pre-Flight Checks
Before pushing the code, please use run the bash script:
```sh
./presubmit.sh
```
this will run the linter and check for license.

To run unit-tests, please run the command:
```sh
pytest -n auto tests/unit
```

# Running Models on VertexAI
In the `experimental` folder use either of the two bash scripts to run a training job.

Each script has a `BUILD_IMAGE` option; if we're building the image for the first time prior to pushing it to the repository, make sure to set `BUILD_IMAGE` to true. This will create the docker image and push it to the repository.

Apart from `BUILD_IMAGE`, we need to also specify the `IMAGE_TAG`, which will be the identifying tag for the image once pushed to the repository. (This can include our username and/or model identifiers)

##### NOTE:

`./experimental/launch_caip_job.sh` can only use images stored in GCR for training, GCR does not offer India (asia-south1) as a region.

`./experimental/launch_custom_job.sh` can use images stored in GCR as well as Artifact Registry for training; this is the *recommended* way of training custom models.