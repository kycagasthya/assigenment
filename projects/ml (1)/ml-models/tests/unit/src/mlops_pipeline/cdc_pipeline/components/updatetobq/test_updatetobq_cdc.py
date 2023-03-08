# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
"""unit test for test_updatetobq_cdc"""

import unittest
import sys
from unittest.mock import patch

sys.path.insert(0, 'src/mlops_pipeline/cdc_pipeline/components/updatetobq/src')
import update_to_bq_cdc


class MockReponse:
    '''
        Mocked response for requests.post and request.get
    '''

    def __init__(self, json_data, status_code, text=None):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.json_data


class Var():
    """ variables used in TestCDC """

    def __init__(self) -> None:
        self.timestamp = '2022-05-13 12:31:37'
        self.bucket_name = 'gs://icici-docai-ia-gcs-redact-dev/cdc_mlops'
        self.project_id = '828122618009'
        self.processor_id = '4fd83649b68e0f12'
        self.location = 'us'
        self.processor_type = 'Custom Document Classifier'
        self.model_version_name = 'v2'
        self.job_id = 'cdc-train-pipeline-202204212022'
        self.check_status_after = '60'
        self.project_number = '828122618009'
        self.pipeline_root = f'{self.bucket_name}/pipelineroot/'
        self.components_dir = '../component'
        self.model_display_name = 'mlops_cdc_comb'
        self.ref_code_file_version = 'bc0328eeaaebb7f3'
        self.model_type = 'classification'
        self.doc_type = 'class'
        self.dataset_model = 'icici_docai_bq'
        self.table_name_model = 'training_model_metrics'
        self.dataset_class = 'icici_docai_bq'
        self.table_name_class = 'training_class_metrics_v2'
        self.version_id = '8dd6356072ab2717'
        self.region = 'asia-south1'
        self.gcs_path = 'gs://ibank-development-transfer-bucket/ML/' \
                        'evaluation/cdc/20220412133453'
        self.gcs_uri = 'gs://ibank-development-transfer-bucket/ML/' \
                       'evaluation/cdc/20220412133453/eval_df.csv'
        self.eval_gcs_path = 'gs://ibank-development-transfer-bucket/ML/' \
                             'evaluation/cdc/'
        self.pipeline_name = 'docai_cdc'
        self.configuration = 'dummy_config'
        self.is_deployed = False
        self.data_pipeline_root = 'dummy_uri'
        self.gcs_path_model = 'NA'
        self.processor_version_name = 'dummy_version_name'
        self.processor_version_id = 'dummy_processor_version_id'
        self.class_dic = {'aadhaar_card_precision': 1.0,
                          'aadhaar_card_f1-score': 0.888888888888889,
                          'aadhaar_card_recall': 0.8,
                          'aadhaar_card_accuracy': 0.8,
                          'voter_card_precision': 0.0,
                          'voter_card_f1-score': 0.0,
                          'voter_card_recall': 0.0,
                          'voter_card_accuracy': 0,
                          'aadhaar_card_tp': 4,
                          'aadhaar_card_tn': 0,
                          'aadhaar_card_fp': 0,
                          'aadhaar_card_fn': 1,
                          'voter_card_tp': 0,
                          'voter_card_tn': 4,
                          'voter_card_fp': 1,
                          'voter_card_fn': 0}

        self.overall_dic = {'test_precision': 1,
                            'test_f1_score': 1,
                            'test_recall': 1,
                            'golden_precision': 0.5,
                            'golden_f1_score': 0.4444444444444445,
                            'golden_recall': 0.4,
                            'golden_accuracy': 0.8}

        self.train_count_actual = 95
        self.test_count_actual = 53
        self.train_gcs_uri_actual = 'gs://ibank-development-transfer-bucket/' \
                                    'ML/CDC_DATASET/cdc_mlops/metadata/'
        self.jsons_model_actual = [{'model_name': 'mlops_cdc_comb',
                                    'job_id': 'cdc-train-pipeline-202204212022',
                                    'processor_version_id': 'dummy_proces' \
                                                            'sor_version_id',
                                    'model_id': '4fd83649b68e0f12',
                                    'version_name': 'dummy_version_name',
                                    'is_deployed': 'False',
                                    'pipeline_name': 'docai_cdc',
                                    'model_region': 'asia-south1',
                                    'ref_code_file_version': 'bc0328eeaaebb7f3',
                                    'train_test_split': 0,
                                    'train_test_size': {'train': 92,
                                                        'test': 54},
                                    'gcs_ref_training_data': 'gs://ibank-' \
                                            'development-transfer-bucket/ML/' \
                                            'CDC_DATASET/cdc_mlops/metadata/',
                                    'trained_on': '2022-05-13 12:31:37',
                                    'deployed_on': '2022-05-13 12:31:37',
                                    'score': {'golden': {'precision': 0.5,
                                                         'f1_score':
                                                             0.4444444444444445,
                                                         'recall': 0.4,
                                                         'accuracy': 0.8},
                                              'test': {'precision': 1,
                                                       'f1_score': 1,
                                                       'recall': 1}},
                                    'gcs_path_evaluation_csv':
                                        'dummy_uri/evaluation_df.csv',
                                    'gcs_path_model': 'NA',
                                    'configuration': 'dummy_config'}]

        self.json_class_list_actual = [{'model_name': 'mlops_cdc_comb',
                                        'job_id':
                                            'cdc-train-pipeline-202204212022',
                                        'processor_version_id':
                                            'dummy_processor_version_id',
                                        'model_id': '4fd83649b68e0f12',
                                        'version_name': 'dummy_version_name',
                                        'is_deployed': 'False',
                                        'pipeline_name': 'docai_cdc',
                                        'model_region': 'asia-south1',
                                        'doc_type': 'class',
                                        'field': 'aadhaar_card',
                                        'true_positive': '4',
                                        'false_positive': '0',
                                        'true_negative': '0',
                                        'false_negative': '1', 'score': {
                'golden': {'precision': 0.5, 'f1_score': 0.4444444444444445,
                           'recall': 0.4, 'accuracy': 0.8}}},
                                       {'model_name': 'mlops_cdc_comb',
                                        'job_id':
                                            'cdc-train-pipeline-202204212022',
                                        'processor_version_id':
                                            'dummy_processor_version_id',
                                        'model_id': '4fd83649b68e0f12',
                                        'version_name': 'dummy_version_name',
                                        'is_deployed': 'False',
                                        'pipeline_name': 'docai_cdc',
                                        'model_region': 'asia-south1',
                                        'doc_type': 'class',
                                        'field': 'pan_card',
                                        'true_positive': '0',
                                        'false_positive': '0',
                                        'true_negative': '0',
                                        'false_negative': '0', 'score': {
                                           'golden': {'precision': 0.5,
                                                      'f1_score':
                                                          0.4444444444444445,
                                                      'recall': 0.4,
                                                      'accuracy': 0.8}}},
                                       {'model_name': 'mlops_cdc_comb',
                                        'job_id':
                                            'cdc-train-pipeline-202204212022',
                                        'processor_version_id':
                                            'dummy_processor_version_id',
                                        'model_id': '4fd83649b68e0f12',
                                        'version_name': 'dummy_version_name',
                                        'is_deployed': 'False',
                                        'pipeline_name': 'docai_cdc',
                                        'model_region': 'asia-south1',
                                        'doc_type': 'class',
                                        'field': 'driving_license',
                                        'true_positive': '0',
                                        'false_positive': '0',
                                        'true_negative': '0',
                                        'false_negative': '0', 'score': {
                                           'golden': {'precision': 0.5,
                                                      'f1_score':
                                                          0.4444444444444445,
                                                      'recall': 0.4,
                                                      'accuracy': 0.8}}},
                                       {'model_name': 'mlops_cdc_comb',
                                        'job_id':
                                            'cdc-train-pipeline-202204212022',
                                        'processor_version_id':
                                            'dummy_processor_version_id',
                                        'model_id': '4fd83649b68e0f12',
                                        'version_name': 'dummy_version_name',
                                        'is_deployed': 'False',
                                        'pipeline_name': 'docai_cdc',
                                        'model_region': 'asia-south1',
                                        'doc_type': 'class',
                                        'field': 'passport',
                                        'true_positive': '0',
                                        'false_positive': '0',
                                        'true_negative': '0',
                                        'false_negative': '0', 'score': {
                                           'golden': {'precision': 0.5,
                                                      'f1_score':
                                                          0.4444444444444445,
                                                      'recall': 0.4,
                                                      'accuracy': 0.8}}},
                                       {'model_name': 'mlops_cdc_comb',
                                        'job_id':
                                            'cdc-train-pipeline-202204212022',
                                        'processor_version_id':
                                            'dummy_processor_version_id',
                                        'model_id': '4fd83649b68e0f12',
                                        'version_name': 'dummy_version_name',
                                        'is_deployed': 'False',
                                        'pipeline_name': 'docai_cdc',
                                        'model_region': 'asia-south1',
                                        'doc_type': 'class', 'field': 'voter',
                                        'true_positive': '0',
                                        'false_positive': '1',
                                        'true_negative': '4',
                                        'false_negative': '0', 'score': {
                                           'golden': {'precision': 0.5,
                                                      'f1_score':
                                                          0.4444444444444445,
                                                      'recall': 0.4,
                                                      'accuracy': 0.8}}}]
        self.response_json = {'splitStats': [{'type': 'DATASET_SPLIT_TRAIN',
                                              'datasetStats': {
                                                  'documentCount': 95,
                                                  'statsEntries': [{
                                                   'labelingStateKey':
                                                       'DOCUMENT_LABELED',
                                                   'documentCount': 94,
                                                   'instanceCount': 94},
                                               {
                                                   'labelingStateKey':
                                                       'DOCUMENT_UNLABELED',
                                                   'documentCount': 1,
                                                   'instanceCount': 1},
                                               {
                                                   'entityTypeKey':
                                                       'aadhaar_card',
                                                   'documentCount': 13,
                                                   'instanceCount': 13},
                                               {
                                                   'entityTypeKey':
                                                       'driving_license',
                                                   'documentCount': 14,
                                                   'instanceCount': 14},
                                               {
                                                   'entityTypeKey': 'pan_card',
                                                   'documentCount': 25,
                                                   'instanceCount': 25},
                                               {
                                                   'entityTypeKey': 'passport',
                                                   'documentCount': 14,
                                                   'instanceCount': 14},
                                               {
                                                   'entityTypeKey':
                                                       'stay_connected_form',
                                                   'documentCount': 13,
                                                   'instanceCount': 13},
                                               {
                                                   'entityTypeKey':
                                                       'study_permit',
                                                   'documentCount': 2,
                                                   'instanceCount': 2},
                                               {
                                                   'entityTypeKey':
                                                       'voter_card',
                                                   'documentCount': 13,
                                                   'instanceCount': 13}]}},
                                             {'type': 'DATASET_SPLIT_TEST',
                                              'datasetStats': {
                                                  'documentCount': 53,
                                                  'statsEntries': [{
                                                   'labelingStateKey':
                                                       'DOCUMENT_LABELED',
                                                   'documentCount': 53,
                                                   'instanceCount': 53},
                                               {
                                                   'labelingStateKey':
                                                       'DOCUMENT_UNLABELED',
                                                   'documentCount': 1,
                                                   'instanceCount': 1},
                                               {
                                                   'entityTypeKey':
                                                       'aadhaar_card',
                                                   'documentCount': 7,
                                                   'instanceCount': 7},
                                               {
                                                   'entityTypeKey':
                                                       'driving_license',
                                                   'documentCount': 14,
                                                   'instanceCount': 14},
                                               {
                                                   'entityTypeKey':
                                                       'pan_card',
                                                   'documentCount': 7,
                                                   'instanceCount': 7},
                                               {
                                                   'entityTypeKey': 'passport',
                                                   'documentCount': 8,
                                                   'instanceCount': 8},
                                               {
                                                   'entityTypeKey':
                                                       'stay_connected_form',
                                                   'documentCount': 3,
                                                   'instanceCount': 3},
                                               {
                                                   'entityTypeKey':
                                                       'study_permit',
                                                   'documentCount': 1,
                                                   'instanceCount': 1},
                                               {
                                                   'entityTypeKey':
                                                       'voter_card',
                                                   'documentCount': 13,
                                                   'instanceCount': 13}]}},
                                             {
                                                 'type':
                                                     'DATASET_SPLIT_UNASSIGNED',
                                                 'datasetStats': {
                                                     'documentCount': 6,
                                                     'statsEntries': [{
                                                  'labelingStateKey':
                                                      'DOCUMENT_UNLABELED',
                                                  'documentCount': 6,
                                                  'instanceCount': 6},
                                              {
                                                  'entityTypeKey':
                                                      'aadhaar_card'},
                                              {
                                                  'entityTypeKey':
                                                      'driving_license'},
                                              {
                                                  'entityTypeKey': 'pan_card'},
                                              {
                                                  'entityTypeKey': 'passport'},
                                              {
                                                  'entityTypeKey':
                                                      'stay_connected_form'},
                                              {
                                                  'entityTypeKey':
                                                      'study_permit'},
                                              {
                                                  'entityTypeKey':
                                                      'voter_card'}]}}]}


class TestCDC(unittest.TestCase, Var):
    """ testing  update to bq for cdc """
    maxDiff = None

    def __init__(self, *args, **kwargs) -> None:
        """ initiating  VarPath class methods """
        super().__init__(*args, **kwargs)
        Var.__init__(self)

    @patch('update_to_bq_cdc.requests.get')
    def test_get_train_test_size(self, mock_get_response) -> None:
        """ testing  get_train_test_size function """
        json_data = self.response_json
        status_code = 200  # for success
        mock_get_response.return_value = MockReponse(json_data, status_code)

        train_count, test_count = update_to_bq_cdc.get_train_test_size(
            self.project_number,
            self.processor_id,
            self.location)
        train_count_actual = self.train_count_actual
        test_count_actual = self.test_count_actual

        self.assertEqual(train_count, train_count_actual)
        self.assertEqual(test_count, test_count_actual)

    def test_get_train_gcs_uri(self) -> None:
        """ testing  get_train_gcs_uri function """
        train_gcs_uri = update_to_bq_cdc.get_train_gcs_uri(self.project_number,
                                                           self.processor_id,
                                                           self.location)
        train_gcs_uri_actual = self.train_gcs_uri_actual

        self.assertEqual(train_gcs_uri, train_gcs_uri_actual)

    @patch('update_to_bq_cdc.get_train_test_size')
    def test_get_class_model_json(self, mock_get_train_test_size) -> None:
        """ testing  get_class_model_json function """
        mock_get_train_test_size.return_value = 92, 54
        jsons_model, json_class_list = update_to_bq_cdc.get_class_model_json(
            self.model_display_name,
            self.job_id, self.processor_id,
            self.data_pipeline_root,
            self.project_number,
            self.ref_code_file_version,
            self.doc_type,
            self.region, self.timestamp,
            self.pipeline_name,
            self.configuration,
            self.is_deployed,
            self.location,
            self.gcs_path_model,
            self.processor_version_name,
            self.processor_version_id,
            self.class_dic,
            self.overall_dic)

        self.assertEqual(jsons_model, self.jsons_model_actual)
        self.assertEqual(json_class_list, self.json_class_list_actual)
