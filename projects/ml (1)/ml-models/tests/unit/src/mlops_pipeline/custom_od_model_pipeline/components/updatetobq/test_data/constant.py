# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================

class Constant:
    """ constants for test_updatetobq_od """
    timestamp = '2022-05-13 12:31:37'
    model_name = 'mlops_cde_pan'
    job_id = 'et-train-pipeline-20220413192119'
    ref_code_file_version = 'bc0328eeaaebb7f3'
    train_size = 70
    test_size = 30
    doc_type = 'pancard32'
    model_region = 'asia-south1'
    project_id = 'ibank-development'
    dataset_model = 'icici_docai_bq'
    table_name_model = 'training_model_metrics'
    dataset_class = 'icici_docai_bq'
    table_name_class = 'training_class_metrics_v2'
    gcs_path_model = 'alf_test32'
    configuration = '{'test1': 'test2'}'
    pipeline_name = 'pipeline_name'
    model_id = 'model_id'
    version_name = 'version_name'
    is_deployed = False
    data_pipeline_root = 'gs://ibank-development-transfer-bucket/ML' \
                              ''/evaluation/cde/20220412111525/'' \
                              'overall_metrics.json'
    processor_version_id = 'processor_version_id_v2'
    gcs_ref_training_data = 'gs://ibank-development-cde-datasets/' \
                                 'cdc_mlops/training'

    classwise_json_path_data_actual = {'primary_sign': {'TP': 9,
                                                             'FN': 8,
                                                             'FP': 7,
                                                             'TN': 6,
                                                             'accuracy': 0.5,
                                                             'precision': 0.4,
                                                             'recall': 0.3,
                                                             'f1_score': 0.2},
                                            'holder1_sign': {'TP': 9,
                                                             'FN': 8,
                                                             'FP': 7,
                                                             'TN': 6,
                                                             'accuracy': 0.5,
                                                             'precision': 0.4,
                                                             'recall': 0.3,
                                                             'f1_score': 0.2},
                                            'holder2_sign': {'TP': 9,
                                                             'FN': 8,
                                                             'FP': 7,
                                                             'TN': 6,
                                                             'accuracy': 0.5,
                                                             'precision': 0.4,
                                                             'recall': 0.3,
                                                             'f1_score': 0.2}}

    metrics_json_path_data_actual = {'test': {'map': 0.9},
                                          'golden': {'f1_score': 0.9,
                                                     'precision': 0.8,
                                                     'recall': 0.7,
                                                     'accuracy': 0.6}}

    json_class_list_actual = [{'model_name': 'mlops_cde_pan',
                                    'job_id': 'et-train-pipeline-20220413192119',
                                    'processor_version_id': 'processor_version_id_v2',
                                    'model_id': 'model_id',
                                    'version_name': 'version_name',
                                    'is_deployed': 'False',
                                    'pipeline_name': 'pipeline_name',
                                    'model_region': 'asia-south1',
                                    'doc_type': 'pancard32',
                                    'field': 'primary_sign',
                                    'true_positive': '9',
                                    'false_positive': '7',
                                    'true_negative': '6',
                                    'false_negative': '8',
                                    'score': {'golden': {'accuracy': 0.5,
                                                         'precision': 0.4,
                                                         'recall': 0.3,
                                                         'f1_score': 0.2}}},
                                   {'model_name': 'mlops_cde_pan',
                                    'job_id': 'et-train-pipeline-20220413192119',
                                    'processor_version_id': 'processor_version_id_v2',
                                    'model_id': 'model_id',
                                    'version_name': 'version_name',
                                    'is_deployed': 'False',
                                    'pipeline_name': 'pipeline_name',
                                    'model_region': 'asia-south1',
                                    'doc_type': 'pancard32',
                                    'field': 'holder1_sign',
                                    'true_positive': '9',
                                    'false_positive': '7',
                                    'true_negative': '6',
                                    'false_negative': '8',
                                    'score': {'golden': {'accuracy': 0.5,
                                                         'precision': 0.4,
                                                         'recall': 0.3,
                                                         'f1_score': 0.2}}},
                                   {'model_name': 'mlops_cde_pan',
                                    'job_id': 'et-train-pipeline-20220413192119',
                                    'processor_version_id': 'processor_version_id_v2',
                                    'model_id': 'model_id',
                                    'version_name': 'version_name',
                                    'is_deployed': 'False',
                                    'pipeline_name': 'pipeline_name',
                                    'model_region': 'asia-south1',
                                    'doc_type': 'pancard32',
                                    'field': 'holder2_sign',
                                    'true_positive': '9',
                                    'false_positive': '7',
                                    'true_negative': '6',
                                    'false_negative': '8',
                                    'score': {'golden': {'accuracy': 0.5,
                                                         'precision': 0.4,
                                                         'recall': 0.3,
                                                         'f1_score': 0.2}}}]

    gcs_path_evaluation_csv = 'gs://asia-south1-docai-mlops'

    json_model_actual = [{'model_name': 'mlops_cde_pan',
                               'job_id': 'et-train-pipeline-20220413192119',
                               'processor_version_id': 'processor_version_id_v2',
                               'model_id': 'model_id',
                               'version_name': 'version_name',
                               'is_deployed': 'False',
                               'pipeline_name': 'pipeline_name',
                               'model_region': 'asia-south1',
                               'ref_code_file_version': 'bc0328eeaaebb7f3',
                               'train_test_split': 70,
                               'train_test_size': {'train': 70, 'test': 30},
                               'gcs_ref_training_data': 'gs://ibank-development-' \
                               'cde-datasets/cdc_mlops/training',
                               'trained_on': '2022-05-13 12:31:37',
                               'deployed_on': '2022-05-13 12:31:37',
                               'score': {'test': {'map': 0.9},
                                         'golden': {'f1_score': 0.9,
                                                    'precision': 0.8,
                                                    'recall': 0.7,
                                                    'accuracy': 0.6}},
                               'gcs_path_evaluation_csv': 'gs://asia-south1-docai-mlops',
                               'gcs_path_model': 'alf_test32',
                               'configuration': '{"test1": "test2"}'}]

    train_test_count = {'train_size': 8, 'test_size': 2}
