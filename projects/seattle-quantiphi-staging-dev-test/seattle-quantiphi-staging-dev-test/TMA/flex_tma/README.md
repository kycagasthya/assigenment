# **TMA Dataflow Flex Template**
### File highlighting steps to follow to create a flex Template, run a Dataflow job and the parameters associated with it.

## **Create Dataflow Template and Run Dataflow Job**
* ## **Create Dataflow Template**
#### To create the Dataflow Template , execute the below shell script in the Terminal:
**Note:** Please ignore this step if the template is already built.
```
/bin/bash build_flex_template_tma.sh
```

* ## **Run Dataflow Job**

Execute the below command in the current directory on the terminal:

```
/bin/bash run_dataflow_flex_job_tma.sh
```
Example gcloud command to run a dataflow job:
```
gcloud dataflow flex-template run dev-flex-tma-v4 \
--template-file-gcs-location "seagen_dataflow/templates/dev_tma/v4.json" \
--parameters config_file="gs://seagen_dataflow/dev_config_tma4/config.json" \
--parameters input_path="gs://seagen_dataflow/input_csvs/file_30.csv" \
--parameters output_path="gs://seagen_dataflow/results_runner/output-dev-tma-flex4" \
--region "us-west1" \
--subnetwork "regions/us-west1/subnetworks/oregon-subnet"
```
