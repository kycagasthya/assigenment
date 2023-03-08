# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================

"""This module has unit test for evaluate_cde"""

import sys
from os.path import dirname, abspath
import unittest
from unittest.mock  import patch
import pandas as pd
import ast
sys.path.insert(0, 'src/mlops_pipeline/cde_pipeline/components/evaluation/src')
from evaluate_cde import get_url, deploy, undeploy, check_status, CdeEvaluate,\
                     lro, get_test_metrics, processor_deployment, evaluation
current_dir = abspath(dirname(__file__))


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


class Credentials:

    def __init__(self):
        self.token = 'TOKEN'

    def refresh(self, auth_request):
        pass


class VersionName:
    metadata = {'processor_version_id': 'my_version_id',
                'version_name': 'my_version_name'}


class ClassMetrics:

    def log_metric(self, key, value):
        pass


class OverallMetrics:

    def log_metric(self, key, value):
        pass


class TestEvaluate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project_number = 'PROJECT_NUMBER'
        cls.processor_id = 'PROCESSOR_ID'
        cls.version_id = 'VERSION_ID'
        cls.location = 'LOCATION'
        cls.url_substring = 'URL_SUBSTRING'
        cls.lro_name = 'LRO_NAME'
        cls.check_status_after = '60'
        cls.retry_count = 10
        cls.gcs_uri = 'gs://gcs_uri.csv'
        cls.data_pipeline_root = 'gs://data_pipeline_root'
        cls.parser_keys = "['name','fathers_name','dob','pan_id']"
        cls.ground_truth_csv = 'gs://ground_truth_csv.csv'
        cls.doc_type = 'DOC_TYPE'
        cls.eval_df = pd.read_csv(
            f'{current_dir}/test_data/ground_truth.csv')[:1]
        cls.test_metrics = {'precision': 1, 'recall': 1, 'f1_score': 1}
        cls.golden_metrics = {'accuracy': 0.98,
                              'precision': 0.6666666666666666,
                              'recall': 0.6533333333333333,
                              'f1_score': 0.6598639455782312}
        cls.cm_metrics = {'name': {'true_positive': 0, 'false_negative': 0,
                                   'false_positive': 20, 'true_negative': 0},
                          'fathers_name': {'true_positive': 8,
                                           'false_negative': 0,
                                           'false_positive': 12,
                                           'true_negative': 0},
                          'dob': {'true_positive': 20, 'false_negative': 0,
                                  'false_positive': 0, 'true_negative': 0},
                          'pan_id': {'true_positive': 13, 'false_negative': 0,
                                     'false_positive': 7, 'true_negative': 0}}
        cls.classwise_metrics = {'name': {'true_positive': 0,
                                          'false_negative': 0,
                                          'false_positive': 20,
                                          'true_negative': 0,
                                          'accuracy': 0.0,
                                          'precision': 0.0,
                                          'recall': 0,
                                          'f1_score': 0},
                                 'fathers_name': {'true_positive': 8,
                                                  'false_negative': 0,
                                                  'false_positive': 12,
                                                  'true_negative': 0,
                                                  'accuracy': 0.4,
                                                  'precision': 0.4,
                                                  'recall': 1.0,
                                                  'f1_score': 0.57142855},
                                 'dob': {'true_positive': 20,
                                         'false_negative': 0,
                                         'false_positive': 0,
                                         'true_negative': 0,
                                         'accuracy': 1.0,
                                         'precision': 1.0,
                                         'recall': 1.0,
                                         'f1_score': 1.0},
                                 'pan_id': {'true_positive': 13,
                                            'false_negative': 0,
                                            'false_positive': 7,
                                            'true_negative': 0,
                                            'accuracy': 0.65,
                                            'precision': 0.65,
                                            'recall': 1.0,
                                            'f1_score': 0.787878787878788}}


    @patch('evaluate_cde.google.auth.transport.requests.Request')
    @patch('evaluate_cde.google.auth.default')
    @patch('evaluate_cde.requests.post')
    def test_deploy(self, mock_post_response, default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'
        mock_post_response.return_value = MockReponse('None', 200)

        _, token = get_url(self.location, self.url_substring)

        self.assertEqual(token, 'TOKEN')

        response = deploy(self.project_number, self.processor_id,
                          self.location, self.version_id)
        self.assertEqual(response.status_code, 200)


    @patch('evaluate_cde.google.auth.transport.requests.Request')
    @patch('evaluate_cde.google.auth.default')
    @patch('evaluate_cde.requests.post')
    def test_undeploy(self, mock_post_response, default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'
        mock_post_response.return_value = MockReponse('None', 200)

        response = undeploy(self.project_number, self.processor_id,
                          self.location, self.version_id)
        self.assertEqual(response.status_code, 200)


    @patch('evaluate_cde.google.auth.transport.requests.Request')
    @patch('evaluate_cde.google.auth.default')
    @patch('evaluate_cde.requests.get')
    def test_lro_success(self,  mock_get_response, default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        ## test case for SUCCEEDED
        json_data ={'name': 'projects/828122618009/locations/us/operations/\
13598837941472044069',
                    'metadata': {'@type': 'type.googleapis.com/\
google.cloud.documentai.uiv1beta3.DeployProcessorVersionMetadata',
                    'commonMetadata': {'state': 'SUCCEEDED',
                    'createTime': '2022-05-16T10:33:31.744759Z',
                    'updateTime': '2022-05-16T10:33:31.744759Z',
                    'resource': 'projects/828122618009/locations/us/\
processors/4fd83649b68e0f12/processorVersions/16dcb57b63f2ef30'}}}
        status_code = 200
        mock_get_response.return_value = MockReponse(json_data, status_code)

        status = lro(self.lro_name, self.location, self.check_status_after)
        self.assertEqual(status, 'SUCCEEDED')


    @patch('evaluate_cde.google.auth.transport.requests.Request')
    @patch('evaluate_cde.google.auth.default')
    @patch('evaluate_cde.requests.get')
    def test_lro_error(self,  mock_get_response, default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        ## test case for FAILED
        json_data ={'name': 'projects/828122618009/locations/us/operations/\
13598837941472044069',
                    'metadata': {'@type': 'type.googleapis.com/\
google.cloud.documentai.uiv1beta3.DeployProcessorVersionMetadata',
                    'commonMetadata': {'state': 'FAILED',
                    'createTime': '2022-05-16T10:33:31.744759Z',
                    'updateTime': '2022-05-16T10:33:31.744759Z',
                    'resource': 'projects/828122618009/locations/us/\
processors/4fd83649b68e0f12/processorVersions/16dcb57b63f2ef30'}}}
        status_code = 200
        error_msg = 'The Deploy-job has FAILED'
        mock_get_response.return_value = MockReponse(json_data, status_code)

        try:
            _ = lro(self.lro_name, self.location, self.check_status_after)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)

        ## test case for CANCELLED
        json_data ={'name': 'projects/828122618009/locations/us/operations/\
13598837941472044069',
                    'metadata': {'@type': 'type.googleapis.com/\
google.cloud.documentai.uiv1beta3.DeployProcessorVersionMetadata',
                    'commonMetadata': {'state': 'CANCELLED',
                    'createTime': '2022-05-16T10:33:31.744759Z',
                    'updateTime': '2022-05-16T10:33:31.744759Z',
                    'resource': 'projects/828122618009/locations/us/\
processors/4fd83649b68e0f12/processorVersions/16dcb57b63f2ef30'}}}
        status_code = 200
        error_msg = 'The Deploy-job has been CANCELLED'
        mock_get_response.return_value = MockReponse(json_data, status_code)

        try:
            _ = lro(self.lro_name, self.location, self.check_status_after)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


    @patch('evaluate_cde.google.auth.transport.requests.Request')
    @patch('evaluate_cde.google.auth.default')
    @patch('evaluate_cde.requests.get')
    def test_get_test_metrics(self, mock_get_response, default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        json_data ={'name': 'projects/828122618009/locations/us/processors/\
4fd83649b68e0f12/processorVersions/60e8a8a819d02b5c',
                    'displayName': 'v19',
                    'state': 'UNDEPLOYED',
                    'createTime': '2022-05-12T14:53:18.721239Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/60e8a8a819d02b5c/\
evaluations/a9b4218b7c1b85f4',
                    'aggregateMetrics': {'precision': 1, 'recall': 1,
                                         'f1Score': 1}}}

        status_code = 200
        mock_get_response.return_value = MockReponse(json_data, status_code)

        test_metrics = get_test_metrics(self.project_number, self.processor_id,
                          self.location, self.version_id)
        self.assertEqual(test_metrics, {'precision': 1, 'recall': 1,
                                        'f1_score': 1})


    @patch('evaluate_cde.google.auth.transport.requests.Request')
    @patch('evaluate_cde.google.auth.default')
    @patch('evaluate_cde.requests.get')
    def test_check_status(self, mock_get_response, default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        json_data ={'processorVersions': [{'name': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/ddac7abbeaa4c28c',
                    'displayName': 'v28',
                    'state': 'UNDEPLOYED',
                    'createTime': '2022-05-17T14:09:08.701466Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/ddac7abbeaa4c28c/\
evaluations/ff271def79ef63b1',
                    'aggregateMetrics': {'precision': 1,
                     'recall': 0.98039216,
                     'f1Score': 0.99009895}}},
                    {'name': 'projects/828122618009/locations/us/processors/\
4fd83649b68e0f12/processorVersions/8c017df4b90be374',
                    'displayName': 'v27',
                    'state': 'UNDEPLOYED',
                    'createTime': '2022-05-17T11:47:50.306339Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/8c017df4b90be374/\
evaluations/c48f66d6d70aae3',
                    'aggregateMetrics': {'precision': 1, 'recall': 1,
                                         'f1Score': 1}}}]}

        status_code = 200
        mock_get_response.return_value = MockReponse(json_data, status_code)

        state = check_status(self.project_number, self.processor_id,
                          'ddac7abbeaa4c28c', self.location)
        self.assertEqual(state, 'UNDEPLOYED')


    @patch('evaluate_cde.google.auth.transport.requests.Request')
    @patch('evaluate_cde.google.auth.default')
    @patch('evaluate_cde.requests.post')
    @patch('evaluate_cde.requests.get')
    def test_processor_deployment_success(self, mock_get_response,
                                          mock_post_response, default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        # Current state: DEPLOYED
        deploy_state = processor_deployment(self.project_number,
                                            self.processor_id,
                                            self.version_id,
                                            self.location,
                                            self.check_status_after,
                                            self.retry_count,
                                            'DEPLOYED')
        self.assertEqual(deploy_state, 'DEPLOYED')

        # Current state: DEPLOYING
        json_data ={'processorVersions': [{'name': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/ddac7abbeaa4c28c',
                    'displayName': 'v28',
                    'state': 'DEPLOYED',
                    'createTime': '2022-05-17T14:09:08.701466Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/ddac7abbeaa4c28c/\
evaluations/ff271def79ef63b1',
                    'aggregateMetrics': {'precision': 1,
                     'recall': 0.98039216,
                     'f1Score': 0.99009895}}},
                    {'name': 'projects/828122618009/locations/us/processors/\
4fd83649b68e0f12/processorVersions/8c017df4b90be374',
                    'displayName': 'v27',
                    'state': 'UNDEPLOYED',
                    'createTime': '2022-05-17T11:47:50.306339Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/8c017df4b90be374/\
evaluations/c48f66d6d70aae3',
                    'aggregateMetrics': {'precision': 1, 'recall': 1,
                                         'f1Score': 1}}}]}

        status_code = 200
        mock_get_response.return_value = MockReponse(json_data, status_code)

        deploy_state = processor_deployment(self.project_number,
                                            self.processor_id,
                                            'ddac7abbeaa4c28c',
                                            self.location,
                                            self.check_status_after,
                                            self.retry_count,
                                            'DEPLOYING')
        self.assertEqual(deploy_state, 'DEPLOYED')

        # Current state: UNDEPLOYED
        json_data ={'name': 'projects/828122618009/locations/us/operations/\
13598837941472044069',
                    'metadata': {'@type': 'type.googleapis.com/\
google.cloud.documentai.uiv1beta3.DeployProcessorVersionMetadata',
                    'commonMetadata': {'state': 'SUCCEEDED',
                    'createTime': '2022-05-16T10:33:31.744759Z',
                    'updateTime': '2022-05-16T10:33:31.744759Z',
                    'resource': 'projects/828122618009/locations/us/\
processors/4fd83649b68e0f12/processorVersions/16dcb57b63f2ef30'}}}
        status_code = 200
        mock_get_response.return_value = MockReponse(json_data, status_code)
        json_data ={'name': 'projects/828122618009/locations/us/operations/\
4520543778093872889',
                    'metadata': {'@type': 'type.googleapis.com/\
google.cloud.documentai.uiv1beta3.DeployProcessorVersionMetadata',
                    'commonMetadata': {'state': 'RUNNING',
                    'createTime': '2022-05-16T10:39:58.199845Z',
                    'updateTime': '2022-05-16T10:39:58.199845Z',
                    'resource': 'projects/828122618009/locations/us/\
processors/4fd83649b68e0f12/processorVersions/60e8a8a819d02b5c'}}}
        mock_post_response.return_value = MockReponse(json_data, status_code)

        deploy_state = processor_deployment(self.project_number,
                                            self.processor_id,
                                            self.version_id,
                                            self.location,
                                            self.check_status_after,
                                            self.retry_count,
                                            'UNDEPLOYED')
        self.assertEqual(deploy_state, 'DEPLOYED')


    @patch('evaluate_cde.google.auth.transport.requests.Request')
    @patch('evaluate_cde.google.auth.default')
    @patch('evaluate_cde.requests.get')
    @patch('evaluate_cde.time.sleep')
    def test_processor_deployment_error(self, mock_time, mock_get_response,
                                        default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        json_data ={'processorVersions': [{'name': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/ddac7abbeaa4c28c',
                    'displayName': 'v28',
                    'state': 'DEPLOYING',
                    'createTime': '2022-05-17T14:09:08.701466Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/ddac7abbeaa4c28c/\
evaluations/ff271def79ef63b1',
                    'aggregateMetrics': {'precision': 1,
                     'recall': 0.98039216,
                     'f1Score': 0.99009895}}},
                    {'name': 'projects/828122618009/locations/us/processors/\
4fd83649b68e0f12/processorVersions/8c017df4b90be374',
                    'displayName': 'v27',
                    'state': 'UNDEPLOYED',
                    'createTime': '2022-05-17T11:47:50.306339Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/8c017df4b90be374/\
evaluations/c48f66d6d70aae3',
                    'aggregateMetrics': {'precision': 1, 'recall': 1,
                                         'f1Score': 1}}}]}

        status_code = 200
        mock_get_response.return_value = MockReponse(json_data, status_code)
        mock_time.return_value = None
        error_msg = 'Model not in deployed state'

        try:
            _ = processor_deployment(self.project_number,
                                     self.processor_id,
                                     'ddac7abbeaa4c28c',
                                     self.location,
                                     self.check_status_after,
                                     self.retry_count,
                                     'DEPLOYING')
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


    @patch('evaluate_cde.pd.read_csv')
    @patch('evaluate_cde.gcsfs.GCSFileSystem')
    @patch('evaluate_cde.helpers.OnlinePred')
    def test_evaluate_cde(self, mock_online_pred, mock_gcsfilesystem, mock_df):
        mock_df.return_value = self.eval_df
        mock_online_pred().predict_cde.return_value = [
            {'key': 'name', 'value': 'HEER SAVANT', 'confidence': 0.95},
            {'key': 'fathers_name', 'value': 'TANYA DADA', 'confidence': 0.95},
            {'key': 'dob', 'value': '01/06/2017', 'confidence': 0.95},
            {'key': 'pan_id', 'value': 'IGBPL9183R', 'confidence': 0.95}
        ]
        with open(f'{current_dir}/test_data/sample_img.png',
                  'rb') as sample_image:
            mock_gcsfilesystem().open.return_value = sample_image
            parser_keys = ast.literal_eval(self.parser_keys)
            cde_eval = CdeEvaluate(self.project_number,
                                   self.processor_id,
                                   self.version_id,
                                   self.location,
                                   parser_keys,
                                   self.ground_truth_csv,
                                   self.doc_type)

            output = cde_eval.evaluate()
            self.assertEqual(len(output), 4)


    @patch('evaluate_cde.undeploy')
    @patch('evaluate_cde.pd.DataFrame.to_csv')
    @patch('evaluate_cde.CdeEvaluate')
    @patch('evaluate_cde.get_test_metrics')
    @patch('evaluate_cde.processor_deployment')
    @patch('evaluate_cde.check_status')
    def test_evaluation(self, mock_check_status, mock_processor_deployment,
                        mock_get_test_metrics, mock_cde_evaluate,
                        mock_df, mock_undeploy):
        mock_check_status.return_value = 'DEPLOYED'
        mock_processor_deployment.return_value = 'DEPLOYED'
        mock_get_test_metrics.return_value = self.test_metrics
        mock_cde_evaluate().evaluate.return_value = self.eval_df, \
        self.golden_metrics, self.cm_metrics, self.classwise_metrics
        mock_df.return_value = None
        mock_undeploy.return_value = MockReponse('None', 200)

        evaluation(self.project_number, self.processor_id, self.location,
                   self.data_pipeline_root, VersionName(), self.parser_keys,
                   self.ground_truth_csv, self.doc_type,
                   self.check_status_after, self.retry_count,
                   OverallMetrics(), ClassMetrics())


if __name__ == '__main__':
    unittest.main()
