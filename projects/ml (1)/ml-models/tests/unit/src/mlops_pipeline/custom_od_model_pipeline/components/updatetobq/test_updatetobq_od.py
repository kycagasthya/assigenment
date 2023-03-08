# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================
"""test py file for update to bq of the custom od"""
import unittest
import sys
from unittest.mock import patch
from os.path import dirname, abspath
sys.path.insert(0,
                'src/mlops_pipeline/custom_od_model_pipeline/'  \
                'components/updatetobq/src')
import update_to_bq_od

current_dir = abspath(dirname(__file__))


class OverallMetrics:
    """ OverallMetrics to mock the value of overall metrics"""
    metadata = {'f1_score': 0.9, 'precision': 0.8, 'recall': 0.7,
                'accuracy': 0.6}


class ClasswiseMetrics:
    """ ClasswiseMetrics to mock the value of classwise metrics"""
    metadata = {'primary_tp': 9, 'primary_fn': 8, 'primary_fp': 7,
                'primary_tn': 6, 'primary_accuracy': 0.5,
                'primary_precision': 0.4, 'primary_recall': 0.3,
                'primary_f1_score': 0.2,
                'holder1_tp': 9, 'holder1_fn': 8, 'holder1_fp': 7,
                'holder1_tn': 6, 'holder1_accuracy': 0.5,
                'holder1_precision': 0.4, 'holder1_recall': 0.3,
                'holder1_f1_score': 0.2,
                'holder2_tp': 9, 'holder2_fn': 8, 'holder2_fp': 7,
                'holder2_tn': 6, 'holder2_accuracy': 0.5,
                'holder2_precision': 0.4, 'holder2_recall': 0.3,
                'holder2_f1_score': 0.2}


class OverallMetricsModel:
    """ OverallMetricsModel to mock the value of overall metrics model"""
    metadata = {'best_map': 0.9}


class Var():
    """ Used for defining actuals and values for test """

    def __init__(self) -> None:
        self.timestamp = '2022-05-13 12:31:37'
        self.model_name = 'mlops_cde_pan'
        self.job_id = 'et-train-pipeline-20220413192119'
        self.ref_code_file_version = 'bc0328eeaaebb7f3'
        self.train_size = 70
        self.test_size = 30
        self.doc_type = 'pancard32'
        self.model_region = 'asia-south1'
        self.project_id = 'ibank-development'
        self.dataset_model = 'icici_docai_bq'
        self.table_name_model = 'training_model_metrics'
        self.dataset_class = 'icici_docai_bq'
        self.table_name_class = 'training_class_metrics_v2'
        self.gcs_path_model = 'alf_test32'
        self.configuration = '{"test1": "test2"}'
        self.pipeline_name = 'pipeline_name'
        self.model_id = 'model_id'
        self.version_name = 'version_name'
        self.is_deployed = False
        self.data_pipeline_root = 'gs://ibank-development-transfer-bucket/ML' \
                                  '/evaluation/cde/20220412111525/' \
                                  'overall_metrics.json'
        self.processor_version_id = 'processor_version_id_v2'
        self.gcs_ref_training_data = 'gs://ibank-development-cde-datasets/' \
                                     'cdc_mlops/training'

        self.classwise_json_path_data_actual = {'primary_sign': {'TP': 9,
                                                                 'FN': 8,
                                                                 'FP': 7,
                                                                 'TN': 6,
                                                                 'accuracy':
                                                                    0.5,
                                                                 'precision':
                                                                    0.4,
                                                                 'recall': 0.3,
                                                                 'f1_score':
                                                                    0.2},
                                                'holder1_sign': {'TP': 9,
                                                                 'FN': 8,
                                                                 'FP': 7,
                                                                 'TN': 6,
                                                                 'accuracy':
                                                                    0.5,
                                                                 'precision':
                                                                    0.4,
                                                                 'recall':
                                                                    0.3,
                                                                 'f1_score':
                                                                    0.2},
                                                'holder2_sign': {'TP': 9,
                                                                 'FN': 8,
                                                                 'FP': 7,
                                                                 'TN': 6,
                                                                 'accuracy':
                                                                    0.5,
                                                                 'precision':
                                                                    0.4,
                                                                 'recall': 0.3,
                                                                 'f1_score':
                                                                     0.2}}

        self.metrics_json_path_data_actual = {'test': {'map': 0.9},
                                              'golden': {'f1_score': 0.9,
                                                         'precision': 0.8,
                                                         'recall': 0.7,
                                                         'accuracy': 0.6}}

        self.json_class_list_actual = [{'model_name': 'mlops_cde_pan',
                                        'job_id':
                                        'et-train-pipeline-20220413192119',
                                        'processor_version_id':
                                        'processor_version_id_v2',
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
                                        'job_id':
                                        'et-train-pipeline-20220413192119',
                                        'processor_version_id':
                                        'processor_version_id_v2',
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
                                        'job_id':
                                        'et-train-pipeline-20220413192119',
                                        'processor_version_id':
                                        'processor_version_id_v2',
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

        self.gcs_path_evaluation_csv = 'gs://asia-south1-docai-mlops'

        self.json_model_actual = [{'model_name': 'mlops_cde_pan',
                                   'job_id': 'et-train-pipeline-20220413192119',
                                   'processor_version_id':
                                    'processor_version_id_v2',
                                   'model_id': 'model_id',
                                   'version_name': 'version_name',
                                   'is_deployed': 'False',
                                   'pipeline_name': 'pipeline_name',
                                   'model_region': 'asia-south1',
                                   'ref_code_file_version': 'bc0328eeaaebb7f3',
                                   'train_test_split': 70,
                                   'train_test_size': {'train': 70, 'test': 30},
                                   'gcs_ref_training_data':
                                    'gs://ibank-development-cde-datasets/'  \
                                    'cdc_mlops/training',
                                   'trained_on': '2022-05-13 12:31:37',
                                   'deployed_on': '2022-05-13 12:31:37',
                                   'score': {'test': {'map': 0.9},
                                             'golden': {'f1_score': 0.9,
                                                        'precision': 0.8,
                                                        'recall': 0.7,
                                                        'accuracy': 0.6}},
                                   'gcs_path_evaluation_csv':
                                    'gs://asia-south1-docai-mlops',
                                   'gcs_path_model': 'alf_test32',
                                   'configuration': "{'test1': 'test2'}"}]

        self.train_test_count = {'train_size': 8, 'test_size': 2}


class TestCDC(unittest.TestCase, Var):
    maxDiff = None

    def __init__(self, *args, **kwargs) -> None:
        """ initiating  VarPath class methods """
        super().__init__(*args, **kwargs)
        Var.__init__(self)

    @classmethod
    def setUpClass(cls):
        cls.Input = 'Input'

    def test_get_train_test_size(self) -> None:
        train_size_actual = 8
        test_size_actual = 2
        train_size, test_size = update_to_bq_od.get_train_test_size(
            self.train_test_count)
        self.assertEqual(train_size_actual, train_size)
        self.assertEqual(test_size_actual, test_size)

    def test_get_classwise_metrics(self) -> None:
        classwise_json_path_data_actual = self.classwise_json_path_data_actual
        metrics_json_path_data_actual = self.metrics_json_path_data_actual
        classwise_json_path_data, metrics_json_path_data = update_to_bq_od. \
            get_classwise_metrics(
            OverallMetrics(),
            ClasswiseMetrics(),
            OverallMetricsModel())

        self.assertEqual(classwise_json_path_data,
                         classwise_json_path_data_actual)
        self.assertEqual(metrics_json_path_data, metrics_json_path_data_actual)

    def test_get_json_class(self) -> None:
        json_class_list = update_to_bq_od.get_json_class(
            self.model_name,
            self.job_id,
            self.doc_type,
            self.model_region,
            self.model_id,
            self.version_name,
            self.is_deployed,
            self.classwise_json_path_data_actual,
            self.pipeline_name,
            self.processor_version_id,
            )
        json_class_list_actual = self.json_class_list_actual

        self.assertEqual(json_class_list, json_class_list_actual)

    def test_get_json_model(self) -> None:
        json_model = update_to_bq_od.get_json_model(
            self.model_name,
            self.job_id,
            self.ref_code_file_version,
            self.model_region,
            self.timestamp,
            self.gcs_path_model,
            self.configuration,
            self.model_id,
            self.version_name,
            self.is_deployed,
            self.gcs_path_evaluation_csv,
            self.pipeline_name,
            self.processor_version_id,
            self.gcs_ref_training_data,
            self.metrics_json_path_data_actual,
            self.train_size,
            self.test_size)

        json_model_actual = self.json_model_actual

        self.assertEqual(json_model, json_model_actual)

    @patch('update_to_bq_od.bigquery.Client')
    @patch('update_to_bq_od.get_train_test_size')
    @patch('update_to_bq_od.get_classwise_metrics')
    @patch('update_to_bq_od.gcsfs.GCSFileSystem')
    def test_write_metrics_to_bq(self, mock_gcsfs_gcfsilesystem,
                                 mock_get_classwise_metrics,
                                 mock_get_train_test_size,
                                 mock_bigquery_client) -> None:
        mock_bigquery_client().insert_rows.return_value = []
        mock_bigquery_client().get_table.return_value = None

        mock_gcsfs_gcfsilesystem().open.return_value = open(
            f'{current_dir}/test_data/'
            f'test_json.json', 'r')
        mock_get_train_test_size.return_value = 8, 2
        mock_get_classwise_metrics.return_value = \
            self.classwise_json_path_data_actual, \
            self.metrics_json_path_data_actual

        update_to_bq_od.write_metrics_to_bq(self.model_name,
                                            self.job_id,
                                            self.ref_code_file_version,
                                            self.doc_type,
                                            self.project_id,
                                            self.model_region,
                                            self.timestamp,
                                            self.dataset_model,
                                            self.table_name_model,
                                            self.dataset_class,
                                            self.table_name_class,
                                            self.configuration,
                                            self.model_id,
                                            self.version_name,
                                            self.is_deployed,
                                            self.data_pipeline_root,
                                            OverallMetrics(),
                                            ClasswiseMetrics(),
                                            OverallMetricsModel(),
                                            self.pipeline_name,
                                            self.processor_version_id,
                                            self.gcs_ref_training_data)
