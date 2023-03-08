# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================

"""This module has unit test for training_cde"""

import sys
import unittest
from unittest.mock import patch
from os.path import dirname, abspath
sys.path.insert(0, 'src/mlops_pipeline/cde_pipeline/components/training/src')
from training_cde import get_auth_token, uptraining, training_from_scratch,   \
                     get_latest_version, get_default_version, training,    \
                     create_version_name, lro, cde_train
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
    metadata = {}


class TestTraining(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project_number = 'PROJECT_NUMBER'
        cls.processor_id = 'PROCESSOR_ID'
        cls.version_id = 'VERSION_ID'
        cls.location = 'LOCATION'
        cls.model_version_name = 'MODEL_VERSION_NAME'
        cls.lro_name = 'LRO_NAME'
        cls.check_status_after = '60'

    ## To DO : add relative path of training later
    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.post')
    def test_uptraining(self, mock_post_response, default, request):
        request.return_value ='AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'
        mock_post_response.return_value = MockReponse('None', 200)

        token, _ = get_auth_token(self.location)
        self.assertEqual(token, 'TOKEN')

        ###Test Uptraining
        response = uptraining(self.project_number, self.processor_id,
                              self.version_id, self.location,
                              self.model_version_name)
        self.assertEqual(response.status_code, 200)


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.post')
    def test_training_from_scratch(self, mock_post_response, default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        json_data = 'None'   ## Add real json response for this request
        status_code = 200

        mock_post_response.return_value =  MockReponse(json_data, status_code)

        response = training_from_scratch(self.project_number,
                                         self.processor_id,
                                         self.location,
                                         self.model_version_name)
        self.assertEqual(response.status_code, 200)


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.get')
    def test_get_latest_version_success(self, mock_get_response,
                                        default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        json_data ={'processorVersions': [{'name': 'projects/828122618009/\
locations/us/processors/12c6c01f2fb2d7f6/processorVersions/my-version-id',
                    'displayName': 'v4',
                    'state': 'DEPLOYED',
                    'createTime': '2022-05-04T08:34:59.282582Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/12c6c01f2fb2d7f6/processorVersions/96a88a695c35d319/\
evaluations/e212c7578803e0aa',
                    'aggregateMetrics': {'precision': 0.9939394,
                     'recall': 0.9828767,
                     'f1Score': 0.9883771}}}]}

        status_code = 200    # for success
        mock_get_response.return_value = MockReponse(json_data, status_code)

        version_id = get_latest_version(self.project_number,
                                        self.processor_id, self.location)
        self.assertEqual(version_id, 'my-version-id')


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.get')
    def test_get_latest_version_error(self, mock_get_response,
                                      default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        #test for KeyError
        json_data ={'processorVersions': [{'name1': 'projects/828122618009/\
locations/us/processors/12c6c01f2fb2d7f6/processorVersions/my-version-id',
                    'displayName': 'v4',
                    'state': 'DEPLOYED',
                    'createTime': '2022-05-04T08:34:59.282582Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/12c6c01f2fb2d7f6/processorVersions/96a88a695c35d319/\
evaluations/e212c7578803e0aa',
                    'aggregateMetrics': {'precision': 0.9939394,
                     'recall': 0.9828767,
                     'f1Score': 0.9883771}}}]}

        status_code = 200
        mock_get_response.return_value = MockReponse(json_data, status_code)
        error_msg = "'name'"

        try:
            _ = get_latest_version(self.project_number, self.processor_id,
                                   self.location)
        except KeyError as error:
            self.assertEqual(str(error), error_msg)

        ## test case for 403
        json_data =None
        status_code = 403
        error_msg = 'The ProjectID is incorrect or doesnot exist'
        text = None
        mock_get_response.return_value = MockReponse(json_data,
                                                     status_code, text)

        try:
            _ = get_latest_version(self.project_number,
                                   self.processor_id, self.location)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)

        # test case for 404
        json_data =None
        status_code = 404
        error_msg = 'The ProcessorID is incorrect or doesnot exist'
        text = None
        mock_get_response.return_value = MockReponse(json_data,
                                                     status_code, text)

        try:
            _ = get_latest_version(self.project_number,
                                   self.processor_id, self.location)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)

        # test case for 400
        json_data =None
        status_code = 400
        error_msg = 'Unknown error'
        text = 'error'
        mock_get_response.return_value = MockReponse(json_data,
                                                     status_code, text)

        try:
            _ = get_latest_version(self.project_number,
                                   self.processor_id, self.location)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.get')
    def test_get_default_version_success(self, mock_get_response,
                                         default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        json_data ={'name': 'projects/828122618009/locations/us/\
processors/4fd83649b68e0f12',
                    'type': 'CUSTOM_CLASSIFICATION_PROCESSOR',
                    'displayName': 'mlops_cde',
                    'state': 'ENABLED',
                    'processEndpoint': 'https://us-documentai.googleapis.com/\
v1/projects/828122618009/locations/us/processors/4fd83649b68e0f12:process',
                    'createTime': '2022-04-11T10:47:08.774885Z',
                    'defaultProcessorVersion': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/my-version-id'}

        status_code = 200    # for success
        mock_get_response.return_value = MockReponse(json_data, status_code)

        version_id = get_default_version(self.project_number,
                                         self.processor_id, self.location)
        self.assertEqual(version_id, 'my-version-id')


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.get')
    def test_get_default_version_error(self, mock_get_response,
                                       default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        #test for KeyError
        json_data ={'name': 'projects/828122618009/locations/us/processors/\
4fd83649b68e0f12',
                    'type': 'CUSTOM_CLASSIFICATION_PROCESSOR',
                    'displayName': 'mlops_cde',
                    'state': 'ENABLED',
                    'processEndpoint': 'https://us-documentai.googleapis.com/\
v1/projects/828122618009/locations/us/processors/4fd83649b68e0f12:process',
                    'createTime': '2022-04-11T10:47:08.774885Z'}

        status_code = 200
        mock_get_response.return_value = MockReponse(json_data, status_code)
        error_msg = "'defaultProcessorVersion'"

        try:
            _ = get_default_version(self.project_number,
                                    self.processor_id, self.location)
        except KeyError as error:
            print(f'ERROR: {str(error)}')
            self.assertEqual(str(error), error_msg)

        ## test case for 403
        json_data =None
        status_code = 403
        error_msg = 'The ProjectID is incorrect or doesnot exist'
        text = None
        mock_get_response.return_value = MockReponse(json_data,
                                                     status_code, text)

        try:
            _ = get_default_version(self.project_number,
                                    self.processor_id, self.location)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)

        # test case for 404
        json_data =None
        status_code = 404
        error_msg = 'The ProcessorID is incorrect or doesnot exist'
        text = None
        mock_get_response.return_value = MockReponse(json_data,
                                                     status_code, text)

        try:
            _ = get_default_version(self.project_number,
                                    self.processor_id, self.location)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)

        # test case for 400
        json_data =None
        status_code = 400
        error_msg = 'Unknown error'
        text = 'error'
        mock_get_response.return_value = MockReponse(json_data,
                                                     status_code, text)

        try:
            _ = get_default_version(self.project_number,
                                    self.processor_id, self.location)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.post')
    @patch('training_cde.requests.get')
    def test_training(self, mock_get_response, mock_post_response,
                      default, request):

        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'
        mock_post_response.return_value = MockReponse('None', 200)
        mock_get_response.return_value = MockReponse('None', 200)

        ###Scenario1: Uptraining with latest version
        json_data ={'processorVersions': [{'name': 'projects/828122618009/\
locations/us/processors/12c6c01f2fb2d7f6/processorVersions/my-version-id',
                    'displayName': 'v4',
                    'state': 'DEPLOYED',
                    'createTime': '2022-05-04T08:34:59.282582Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/12c6c01f2fb2d7f6/processorVersions/96a88a695c35d319/\
evaluations/e212c7578803e0aa',
                    'aggregateMetrics': {'precision': 0.9939394,
                    'recall': 0.9828767,
                    'f1Score': 0.9883771}}}]}
        mock_get_response.return_value = MockReponse(json_data, 200)
        mock_post_response.return_value = MockReponse('None', 200)
        response = training(self.project_number, self.processor_id, 'latest',
                              self.location, self.model_version_name)
        self.assertEqual(response.status_code, 200)

        ###Scenario2: Uptraining with default version
        json_data ={'name': 'projects/828122618009/locations/us/processors/\
4fd83649b68e0f12',
                    'type': 'CUSTOM_CLASSIFICATION_PROCESSOR',
                    'displayName': 'mlops_cde',
                    'state': 'ENABLED',
                    'processEndpoint': 'https://us-documentai.googleapis.com/\
v1/projects/828122618009/locations/us/processors/4fd83649b68e0f12:process',
                    'createTime': '2022-04-11T10:47:08.774885Z',
                    'defaultProcessorVersion': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/my-version-id'}
        mock_get_response.return_value = MockReponse(json_data, 200)
        mock_post_response.return_value = MockReponse('None', 200)
        response = training(self.project_number, self.processor_id, 'default',
                              self.location, self.model_version_name)
        self.assertEqual(response.status_code, 200)

        ###Scenario3: Uptraining with given version_id
        mock_post_response.return_value = MockReponse('None', 200)
        response = training(self.project_number, self.processor_id,
                            self.version_id, self.location,
                            self.model_version_name)
        self.assertEqual(response.status_code, 200)

        ###Scenario4: Training from scratch
        mock_post_response.return_value = MockReponse('None', 200)
        response = training(self.project_number, self.processor_id, 'none',
                              self.location, self.model_version_name)
        self.assertEqual(response.status_code, 200)


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.get')
    def test_create_version_name_success(self, mock_get_response,
                                         default, request):
        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        json_data ={'processorVersions': [{'name': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/8c017df4b90be374',
                    'displayName': 'v27',
                    'state': 'DEPLOYING',
                    'createTime': '2022-05-17T11:47:50.306339Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/8c017df4b90be374/\
evaluations/c48f66d6d70aae3',
                    'aggregateMetrics': {'precision': 1, 'recall': 1,
                                         'f1Score': 1}}},
                    {'name': 'projects/828122618009/locations/us/processors/\
4fd83649b68e0f12/processorVersions/51b8143eddde928',
                    'displayName': 'v26',
                    'state': 'UNDEPLOYED',
                    'createTime': '2022-05-17T11:13:33.914777Z',
                    'latestEvaluation': {'evaluation': 'projects/828122618009/\
locations/us/processors/4fd83649b68e0f12/processorVersions/51b8143eddde928/\
evaluations/6ce3ceb37af5d3da',
                    'aggregateMetrics': {'precision': 1,
                     'recall': 0.98039216,
                     'f1Score': 0.99009895}}}],
                    'nextPageToken': 'CgsIlLX0kwYQ8MjWGA'}

        status_code = 200    # for success
        mock_get_response.return_value = MockReponse(json_data, status_code)

        version_id = create_version_name(self.project_number,
                                         self.processor_id, self.location)
        self.assertEqual(version_id, 'v28')


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.get')
    def test_create_version_name_error(self, mock_get_response,
                                       default, request):

        request.return_value = 'AUTH_REQUEST'
        default.return_value = Credentials(), 'Project ID'

        ## test case for 403
        json_data =None
        status_code = 403
        error_msg = 'The ProjectID is incorrect or doesnot exist'
        text = None
        mock_get_response.return_value = MockReponse(json_data,
                                                     status_code, text)

        try:
            _ = create_version_name(self.project_number, self.processor_id,
                                    self.location)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)

        # test case for 404
        json_data =None
        status_code = 404
        error_msg = 'The ProcessorID is incorrect or doesnot exist'
        text = None
        mock_get_response.return_value = MockReponse(json_data,
                                                     status_code, text)

        try:
            _ = create_version_name(self.project_number,
                                    self.processor_id, self.location)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)

        # test case for 400
        json_data =None
        status_code = 400
        error_msg = 'Unknown error'
        text = 'error'
        mock_get_response.return_value = MockReponse(json_data,
                                                     status_code, text)

        try:
            _ = create_version_name(self.project_number,
                                    self.processor_id, self.location)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.get')
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


    @patch('training_cde.google.auth.transport.requests.Request')
    @patch('training_cde.google.auth.default')
    @patch('training_cde.requests.get')
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
        error_msg = 'The Training-job has FAILED'
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
        error_msg = 'The Training-job has been CANCELLED'
        mock_get_response.return_value = MockReponse(json_data, status_code)

        try:
            _ = lro(self.lro_name, self.location, self.check_status_after)
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


    @patch('training_cde.create_version_name')
    @patch('training_cde.training')
    @patch('training_cde.lro')
    def test_cde_train_success(self, mock_lro, mock_training,
                               mock_create_version_name):
        mock_lro.return_value = 'SUCCEEDED'
        mock_create_version_name.return_value = 'v29'

        json_data ={'name': 'projects/828122618009/locations/us/operations/\
1055235975036076572',
                    'metadata': {'@type': 'type.googleapis.com/\
google.cloud.documentai.uiv1beta3.TrainProcessorVersionMetadata',
                    'commonMetadata': {'state': 'RUNNING',
                    'createTime': '2022-05-19T02:32:13.147417Z',
                    'updateTime': '2022-05-19T02:32:13.147417Z',
                    'resource': 'projects/828122618009/locations/us/\
processors/4fd83649b68e0f12/processorVersions/ea4f387463d05d0'},
                    'trainingDatasetValidation': {},
                    'testDatasetValidation': {}}}
        status_code = 200
        mock_training.return_value = MockReponse(json_data, status_code)

        cde_train(self.project_number, self.processor_id, self.version_id,
                  self.location, self.check_status_after, VersionName())


    @patch('training_cde.create_version_name')
    @patch('training_cde.training')
    def test_cde_train_error(self, mock_training, mock_create_version_name):
        mock_create_version_name.return_value = 'v29'

        status_code = 403
        mock_training.return_value = MockReponse('None', status_code)
        error_msg = 'The ProjectID is incorrect or doesnot exist'

        try:
            cde_train(self.project_number, self.processor_id, self.version_id,
                  self.location, self.check_status_after, VersionName())
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


        status_code = 404
        mock_training.return_value = MockReponse('None', status_code)
        error_msg = 'The ProcessorID is incorrect or doesnot exist'

        try:
            cde_train(self.project_number, self.processor_id, self.version_id,
                  self.location, self.check_status_after, VersionName())
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


        status_code = 429
        mock_training.return_value = MockReponse('None', status_code)
        error_msg = 'Resources has been Exhausted. Please check Quota limit.'

        try:
            cde_train(self.project_number, self.processor_id, self.version_id,
                  self.location, self.check_status_after, VersionName())
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


        status_code = 400
        mock_training.return_value = MockReponse('None', status_code)
        error_msg = 'Unknown error'

        try:
            cde_train(self.project_number, self.processor_id, self.version_id,
                  self.location, self.check_status_after, VersionName())
        except RuntimeError as error:
            self.assertEqual(str(error), error_msg)


if __name__ == '__main__':
    unittest.main()
