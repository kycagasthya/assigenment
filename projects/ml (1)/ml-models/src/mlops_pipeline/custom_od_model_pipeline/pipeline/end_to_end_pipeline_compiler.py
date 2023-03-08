# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================
import os
from kfp.v2 import compiler, dsl
from functools import partial
import kfp
from google_cloud_pipeline_components.v1.custom_job import \
    create_custom_training_job_op_from_component
from jinja2 import Template
from compiler_utils import save_spec_file
import traceback
from custlogger import ml_logger
import subprocess


def get_commit_id() -> str:
    """
    extract latest commit d
    Args:
    Returns:
        output: commit id
    """
    try:
        output = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return ""
    return output.strip().decode("utf-8")


def _load_custom_component(
        components_dir: str, component_name: str) -> kfp.components:
    """
    load component from yaml file
    Args:
        components_dir: component directory
        component_name: name of component
    Returns:
        kubflow component
    """
    component_path = os.path.join(components_dir, component_name,
                                  "component.yaml.jinja")
    with open(component_path, "r") as f:
        component_text = Template(f.read()).render()
    return kfp.components.load_component_from_text(component_text)


def create_custom_od_pipeline(components_dir: str, pipeline_spec_name: str):
    """
    creates vertex ai pipeline
    Args:
        components_dir: component directory
        pipeline_spec_name: pipeline specification json name
    Returns:
    """
    load_custom_component = partial(_load_custom_component,
                                    components_dir=components_dir)
    preprocessing_op = load_custom_component(component_name="preprocess")
    train_eval_op = load_custom_component(component_name="train_eval")
    export_op = load_custom_component(component_name="export_model")
    evaluation_op = load_custom_component(component_name="evaluation")
    updatebq_op = load_custom_component(component_name="updatetobq")

    @dsl.pipeline(name="od-end-to-end-pipeline")
    def pipeline(
            data_pipeline_root: str,  pipeline_config_path: str,
            input_size: str, threshold: str,test_data_path: str,
            train_path: str, validation_path: str, label_path: str,
            ref_code_file_version: str, doc_type: str,
            project_id: str, timestamp_hr: str, dataset_model: str,
            table_name_model: str, dataset_class: str, table_name_class: str,
            configuration: str, model_id: str, version_name: str,
            is_deployed: str, job_id: str, pipeline_name: str,
            processor_version_id: str, model_name: str, region: str):
        od_preprocess_task = preprocessing_op(
            train_path=train_path, validation_path=validation_path,
            label_path=label_path, data_pipeline_root=data_pipeline_root)
        train_eval_job_op = create_custom_training_job_op_from_component(
            train_eval_op, display_name="train-component",
            machine_type="n1-standard-16", accelerator_type="NVIDIA_TESLA_T4",
            accelerator_count=2)
        train_eval_task = train_eval_job_op(
            project=project_id, location=region,
            pipeline_config_path=pipeline_config_path,
            label_map_uri=label_path,
            pipeline_root=data_pipeline_root,
            train_tfrecord=od_preprocess_task.outputs["output_train"],
            val_tfrecord=od_preprocess_task.outputs[
                "output_validation"]).after(od_preprocess_task)
        od_export_task = export_op(
            output_directory=data_pipeline_root,
            input_size=input_size,
            checkpoint=train_eval_task.outputs["best_checkpoint"], ).after(
            train_eval_task)
        od_evaluation_task = evaluation_op(
            saved_model=od_export_task.outputs["deployable_model"],
            threshold=threshold,
            test_data_path=test_data_path,
            out_csv_path=data_pipeline_root).after(od_export_task)
        cde_update_bq = updatebq_op(
            model_name=model_name,
            job_id=job_id,
            ref_code_file_version=ref_code_file_version,
            doc_type=doc_type,
            project_id=project_id,
            model_region=region,
            timestamp=timestamp_hr,
            dataset_model=dataset_model,
            table_name_model=table_name_model,
            dataset_class=dataset_class,
            table_name_class=table_name_class,
            configuration=configuration,
            model_id=model_id,
            version_name=version_name,
            is_deployed=is_deployed,
            data_pipeline_root=data_pipeline_root,
            overall_metrics=od_evaluation_task.outputs["overall"],
            classwise_metrics=od_evaluation_task.outputs["classwise"],
            overall_metrics_model=train_eval_task.outputs["val_metrics"],
            pipeline_name=pipeline_name,
            processor_version_id=processor_version_id,
            gcs_ref_training_data=train_path).after(od_evaluation_task)
    compiler.Compiler().compile(pipeline_func=pipeline,
                                package_path=pipeline_spec_name)


if __name__ == "__main__":
    try:
        pipeline_spec_bucket_path = \
            "gs://asia-south1-docai-mlops-com-4dda2ed4-" \
            "bucket/mlops_pipeline_specs"
        model = "custom_od"
        components_dir = "../components"
        commit_id = get_commit_id()
        local_spec_name = f"custom_od_training_pipeline_{commit_id}.json"
        create_custom_od_pipeline(components_dir, local_spec_name)
        save_spec_file(
            pipeline_spec_bucket_path, commit_id, local_spec_name, model)
    except Exception:
        ml_logger(type_log="ERROR", component="Custom OD-Pipeline compiler",
                  message="Pipeline compilation failed",
                  status_code="500", traceback=traceback.format_exc())
        raise
