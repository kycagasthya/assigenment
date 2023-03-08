# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================

"""This module is end to end compiler for cdc processor"""

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
    extract latest commit id
    Args:
    Returns:
        output: commit id
    """
    try:
        output = subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return ''
    return output.strip().decode('utf-8')

def _load_custom_component(components_dir: str,
                           component_name: str)->kfp.components:
    """
    load component from yaml file
    Args:
        components_dir: component directory
        component_name: name of component
    Returns:
        kubeflow component
    """
    component_path = os.path.join(components_dir, component_name,
                                  'component.yaml.jinja')
    with open(component_path, 'r') as f:
        component_text = Template(f.read()).render()
    return kfp.components.load_component_from_text(component_text)

def create_cdc_pipeline(components_dir: str, pipeline_spec_name: str):
    """
    creates vertex ai pipeline
    Args:
        components_dir: component directory
        pipeline_spec_name: pipeline specification json name
    Returns:
    """
    load_custom_component = partial(_load_custom_component,
                                    components_dir=components_dir)
    training_op = load_custom_component(component_name = 'training')
    evaluation_op = load_custom_component(component_name = 'evaluation')
    updatetobq_op = load_custom_component(component_name = 'updatetobq')

    @dsl.pipeline(name='cdc-train-update-bq-pipeline')
    def pipeline(project_id: str,
                 project_number: str,
                 data_pipeline_root: str,
                 processor_id: str,
                 location: str,
                 check_status_after: str,
                 job_id: str,
                 model_display_name: str,
                 ref_code_file_version: str,
                 doc_type: str,
                 region: str,
                 timestamp_hr: str,
                 dataset_model: str,
                 table_name_model: str,
                 dataset_class: str,
                 table_name_class: str,
                 pipeline_name:str,
                 is_deployed : str,
                 configuration:str,
                 gcs_uri: str,
                 version :str,
                 gcs_path_model: str,
                 retry_count :int
                 ):

        cdc_train_task = training_op(
            project_number = project_number,
            processor_id = processor_id,
            location = location,
            version = version,
            check_status_after = check_status_after
        )
        evaluation_task_cdc = evaluation_op(
            project_id=project_number,
            processor_id=processor_id,
            location=location,
            input_version_id=cdc_train_task.outputs['version_name'],
            gcs_uri=gcs_uri,
            check_status_after=check_status_after,
            data_pipeline_root=data_pipeline_root,
            retry_count = retry_count
        ).after(cdc_train_task)

        cdc_update_bq = updatetobq_op(
            model_display_name=model_display_name,
            job_id=job_id,
            processor_id=processor_id,
            data_pipeline_root=data_pipeline_root,
            project_number=project_number,
            ref_code_file_version=ref_code_file_version,
            doc_type=doc_type,
            project_id=project_id,
            region=region,
            timestamp=timestamp_hr,
            dataset_model=dataset_model,
            table_name_model=table_name_model,
            dataset_class=dataset_class,
            table_name_class=table_name_class,
            pipeline_name=pipeline_name,
            is_deployed=is_deployed,
            configuration=configuration,
            gcs_path_model = gcs_path_model,
            location = location,
            version_name=cdc_train_task.outputs['version_name'],
            overall_metrics=evaluation_task_cdc.outputs['overall_metrics'],
            class_metrics=evaluation_task_cdc.outputs['class_metrics']
        ).after(evaluation_task_cdc)
    compiler.Compiler().compile(
        pipeline_func=pipeline, package_path=pipeline_spec_name)

if __name__ == '__main__':
    try:
        default_spec_path = \
        'gs://asia-south1-docai-mlops-com-4dda2ed4-bucket/mlops_pipeline_specs'
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--pipeline_spec', help='pipeline spec bucket path',
            default=default_spec_path)
        parser.add_argument('--model', help='pipeline spec bucket path',
                            default='cdc')
        args = parser.parse_args()
        pipeline_spec_bucket_path = args.pipeline_spec
        model = args.model
        components_dir = '../components'
        commit_id = get_commit_id()
        local_spec_name = f'cdc_pipeline_{commit_id}.json'
        create_cdc_pipeline(components_dir, local_spec_name)
        save_spec_file(pipeline_spec_bucket_path, commit_id,
                       local_spec_name, model)
    except Exception:
        ml_logger(type_log='ERROR', component='CDC-Pipeline compiler',
                  message='Pipeline compilation failed',
                  status_code='500', traceback=traceback.format_exc())
        raise
