# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================
import argparse
import os
from kfp.v2 import compiler, dsl
from functools import partial
import kfp
from jinja2 import Template
from compiler_utils import save_spec_file
import traceback
from custom_logger import ml_logger
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
    #pylint: disable=redefined-outer-name
    components_dir: str,
    component_name: str) -> kfp.components:
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

def create_cde_pipeline(
    #pylint: disable=redefined-outer-name
    components_dir: str,
    pipeline_spec_name: str):
    """
    creates vertex ai pipeline
    Args:
        components_dir: component directory
        pipeline_spec_name: pipeline specification json name
    Returns:
    """
    load_custom_component = partial(
        _load_custom_component,
        components_dir=components_dir)
    training_op = load_custom_component(component_name = "training")
    evaluation_op = load_custom_component(component_name = "evaluation")
    updatebq_op = load_custom_component(component_name = "updatetobq")

    @dsl.pipeline(name="cde-train-update-bq-pipeline")
    def pipeline(
        retry_count: int,
        check_status_after: str,
        job_id: str,
        version: str,
        processor_id: str,
        project_number: str,
        parser_keys : str,
        ground_truth_csv : str,
        ref_code_file_version: str,
        doc_type: str,
        is_deployed:str,
        configuration:str,
        project_id: str,
        region: str,
        timestamp_hr: str,
        pipeline_name:str,
        dataset_model: str,
        table_name_model: str,
        dataset_class: str,
        table_name_class: str,
        data_pipeline_root:str,
        model_name:str,
        gcs_path_model:str,
        location : str):
        cde_train_task = training_op(
            project_number= project_number,version=version,
                                     processor_id=processor_id,
                                     location=location,
                                     check_status_after=check_status_after)
        version_name_artifact=cde_train_task.outputs["version_name"]
        evaluation_task = evaluation_op(project_id= project_id,
                                        processor_id=processor_id,
                                        retry_count = retry_count,
                                        location=location,
                                        version_name=version_name_artifact,
                                        check_status_after = check_status_after,
                                        parser_keys = parser_keys,
                                       data_pipeline_root = data_pipeline_root,
                                       ground_truth_csv = ground_truth_csv,
                                       doc_type = doc_type, ).after(
            cde_train_task)
        updatebq_op(
            job_id = job_id,
            ref_code_file_version = ref_code_file_version,
             doc_type= doc_type,
            project_id = project_id,
            region = region,
            timestamp = timestamp_hr,
            dataset_model = dataset_model,
            table_name_model = table_name_model,
            dataset_class = dataset_class,
            table_name_class = table_name_class,
            gcs_path_model=gcs_path_model,
            configuration=configuration,
            model_name=model_name,
            data_pipeline_root=data_pipeline_root,
            processor_id = processor_id,
            project_number=project_number,
            is_deployed=is_deployed,
            pipeline_name=pipeline_name,
            location=location,
            version_name = version_name_artifact ,
            overall_metrics = evaluation_task.outputs["overall_metrics"],
            class_metrics = evaluation_task.outputs["class_metrics"],
        ).after(evaluation_task)
    compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path=pipeline_spec_name)


if __name__ == "__main__":
    try:
        default_spec_path = "gs://asia-south1-docai-mlops-com-4dda2ed4-bucket/\
        mlops_pipeline_specs"
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--pipeline_spec", help="pipeline spec bucket path",
            default=default_spec_path)
        parser.add_argument("--model",
                            help="pipeline spec bucket path", default="cde")
        args = parser.parse_args()
        pipeline_spec_bucket_path = args.pipeline_spec
        model = args.model
        components_dir = "../components"
        commit_id = get_commit_id()
        local_spec_name = f"cde_pipeline_{commit_id}.json"
        create_cde_pipeline(components_dir, local_spec_name)
        save_spec_file(pipeline_spec_bucket_path,
                       commit_id, local_spec_name, model)
    except Exception:
        ml_logger(type_log="ERROR", component="CDE-Pipeline compiler",
                  message="Pipeline compilation failed",
                  status_code="500", traceback=traceback.format_exc())
        raise
        