# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================
import unittest
import sys
from unittest.mock import patch
sys.path.insert(0, "src/mlops_pipeline/cde_pipeline/components/updatetobq/src")
import update_to_bq_cde



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

class VersionName:
    metadata = {"version_name": "v60",
                "processor_version_id": "b1c995aa2d4a8b75"}


class OverallMetrics:
    metadata = {"name_precision": 0.0, "name_f1-score": 0, "name_recall": 0,
                "name_accuracy": 0.0, "name_tp": 0, "name_fn": 0, "name_fp": 20,
                "name_tn": 0, "fathers_name_precision": 0.4,
                "fathers_name_f1-score": 0.5714285714285715,
                "fathers_name_recall": 1.0, "fathers_name_accuracy": 0.4,
                "fathers_name_tp": 8, "fathers_name_fn": 0,
                "fathers_name_fp": 12, "fathers_name_tn": 0,
                "dob_precision": 1.0, "dob_f1-score": 1.0, "dob_recall": 1.0,
                "dob_accuracy": 1.0, "dob_tp": 20, "dob_fn": 0, "dob_fp": 0,
                "dob_tn": 0, "pan_id_precision": 0.2,
                "pan_id_f1-score": 0.33333333333333337, "pan_id_recall": 1.0,
                "pan_id_accuracy": 0.2, "pan_id_tp": 4, "pan_id_fn": 0,
                "pan_id_fp": 16, "pan_id_tn": 0}


class ClassMetrics:
    metadata = {"name_precision": 0.0, "name_f1-score": 0, "name_recall": 0,
                "name_accuracy": 0.0, "name_tp": 0, "name_fn": 0, "name_fp": 20,
                "name_tn": 0, "fathers_name_precision": 0.4,
                "fathers_name_f1-score": 0.5714285714285715,
                "fathers_name_recall": 1.0, "fathers_name_accuracy": 0.4,
                "fathers_name_tp": 8, "fathers_name_fn": 0,
                "fathers_name_fp": 12, "fathers_name_tn": 0,
                "dob_precision": 1.0, "dob_f1-score": 1.0, "dob_recall": 1.0,
                "dob_accuracy": 1.0, "dob_tp": 20, "dob_fn": 0, "dob_fp": 0,
                "dob_tn": 0, "pan_id_precision": 0.2,
                "pan_id_f1-score": 0.33333333333333337, "pan_id_recall": 1.0,
                "pan_id_accuracy": 0.2, "pan_id_tp": 4, "pan_id_fn": 0,
                "pan_id_fp": 16, "pan_id_tn": 0}


class Var():

    def __init__(self) -> None:
        self.timestamp = "2022-05-13 12:31:37"
        self.bucket_name = "gs://ibank-development-cde-datasets/cde_mlops"
        self.version = "2cb64625c6c66d0f"
        self.location = "us"
        self.check_status_after = "60"
        self.pipeline_root = f"{self.bucket_name}/pipelineroot/"
        self.components_dir = "../components"
        self.parser_keys = ["name", "fathers_name", "dob", "pan_id", "gcs_uri"]
        self.ground_truth_csv = "gs://ibank-development-transfer-bucket/ML/" \
                                "Data/data-buckets/for_parser_q/for_eval/" \
                                "ground_truth.csv"
        self.doc_type = "pan_card"
        self.gcs_path = "gs://ibank-development-transfer-bucket/ML/" \
                        "evaluation/cde/20220412111525/"
        self.model_display_name = "rad_mlops_cde_pan"
        self.job_id = "et-train-pipeline-20220413192119"
        self.project_name = " ibank-development"
        self.ref_code_file_version = "bc0328eeaaebb7f3"
        self.train_size = "70"
        self.test_size = "30"
        self.doc_type = "pan_card4"
        self.region = "asia-south1"
        self.project_id = "ibank-development"
        self.dataset_model = "icici_docai_bq"
        self.table_name_model = "training_model_metrics"
        self.dataset_class = "icici_docai_bq"
        self.table_name_class = "training_class_metrics_v2"
        self.gcs_path_model = "rad_path"
        self.configuration = "{'test1': 'test2'}"
        self.pipeline_name = "cde_pipeline_eval_bq"
        self.model_id = "model_id"
        self.version_name = "version_name_rad"
        self.is_deployed = "False"
        self.gcs_path_evaluation_csv = "dummy_path"
        self.project_id = "ibank-development"
        self.processor_id = "60b530fb3aa7e18"
        self.version_id = "57ad612170b36c2a"
        self.project_number = "828122618009"
        self.pipeline_name = "CDE"
        self.data_pipeline_root = ""
        self.model_version_name = "v46"
        self.model_name = "rad"
        self.processor_version_id = "asdf"
        self.processor_version_name = "v58"
        self.train_percent = "40"
        self.dataset_uri = "NA"
        self.url_substring = "/uiv1beta3/projects/{project_number}/locations/" \
                             "us/processors/{processor_id}/dataset:getAllDa" \
                             "tasetSplitStats/"
        self.version_name = {"version_name": "v60",
                             "processor_version_id": "b1c995aa2d4a8b75"}
        self.class_dic = {"name_precision": 0.0, "name_f1-score": 0,
                          "name_recall": 0, "name_accuracy": 0.0, "name_tp": 0,
                          "name_fn": 0, "name_fp": 20, "name_tn": 0,
                          "fathers_name_precision": 0.4,
                          "fathers_name_f1-score": 0.5714285714285715,
                          "fathers_name_recall": 1.0,
                          "fathers_name_accuracy": 0.4,
                          "fathers_name_tp": 8, "fathers_name_fn": 0,
                          "fathers_name_fp": 12, "fathers_name_tn": 0,
                          "dob_precision": 1.0, "dob_f1-score": 1.0,
                          "dob_recall": 1.0, "dob_accuracy": 1.0, "dob_tp": 20,
                          "dob_fn": 0, "dob_fp": 0, "dob_tn": 0,
                          "pan_id_precision": 0.2,
                          "pan_id_f1-score": 0.33333333333333337,
                          "pan_id_recall": 1.0, "pan_id_accuracy": 0.2,
                          "pan_id_tp": 4, "pan_id_fn": 0, "pan_id_fp": 16,
                          "pan_id_tn": 0}
        self.overall_dic = {"name_precision": 0.0, "name_f1-score": 0,
                            "name_recall": 0, "name_accuracy": 0.0,
                            "name_tp": 0,
                            "name_fn": 0, "name_fp": 20, "name_tn": 0,
                            "fathers_name_precision": 0.4,
                            "fathers_name_f1-score": 0.5714285714285715,
                            "fathers_name_recall": 1.0,
                            "fathers_name_accuracy": 0.4,
                            "fathers_name_tp": 8, "fathers_name_fn": 0,
                            "fathers_name_fp": 12, "fathers_name_tn": 0,
                            "dob_precision": 1.0, "dob_f1-score": 1.0,
                            "dob_recall": 1.0, "dob_accuracy": 1.0,
                            "dob_tp": 20,
                            "dob_fn": 0, "dob_fp": 0, "dob_tn": 0,
                            "pan_id_precision": 0.2,
                            "pan_id_f1-score": 0.33333333333333337,
                            "pan_id_recall": 1.0, "pan_id_accuracy": 0.2,
                            "pan_id_tp": 4, "pan_id_fn": 0, "pan_id_fp": 16,
                            "pan_id_tn": 0}

        self.url_actual = "https://us-documentai.googleapis.com/uiv1beta3/" \
                          "projects/{project_number}/locations/us/processors/" \
                          "{processor_id}/dataset:getAllDatasetSplitStats/"

        self.train_count_actual = 15
        self.test_count_actual = 10

        self.gcs_uri_actual = "gs://ibank-development-cde-datasets/cde_train/"

        self.main_dict_actual = {"dob": {"precision": 1.0,
                                         "f1-score": 1.0,
                                         "recall": 1.0,
                                         "accuracy": 1.0,
                                         "tp": 20,
                                         "fn": 0,
                                         "fp": 0,
                                         "tn": 0},
                                 "name": {"precision": 0.0,
                                          "f1-score": 0,
                                          "recall": 0,
                                          "accuracy": 0.0,
                                          "tp": 0,
                                          "fn": 0,
                                          "fp": 20,
                                          "tn": 0},
                                 "fathers_name": {"precision": 0.4,
                                                  "f1-score":
                                                    0.5714285714285715,
                                                  "recall": 1.0,
                                                  "accuracy": 0.4,
                                                  "tp": 8,
                                                  "fn": 0,
                                                  "fp": 12,
                                                  "tn": 0},
                                 "pan_id": {"precision": 0.2,
                                            "f1-score": 0.33333333333333337,
                                            "recall": 1.0,
                                            "accuracy": 0.2,
                                            "tp": 4,
                                            "fn": 0,
                                            "fp": 16,
                                            "tn": 0}}

        self.overall_main_dict_actual = '{"golden": {},' \
                                        ' "test": {"precision": 0.2,' \
                                        ' "f1_score": 0.33333333333333337,' \
                                        ' "recall": 1.0, "accuracy": 0.2,' \
                                        ' "tp": 4, "fn": 0, "fp": 16, "tn": 0}}'

        self.response_json = {"splitStats": [{"type": "DATASET_SPLIT_TRAIN",
                              "datasetStats": {"documentCount": 15,
                              "statsEntries": [{"labelingStateKey":
                              "DOCUMENT_LABELED", "documentCount": 15,
                              "instanceCount": 15}, {"entityTypeKey": "dob",
                              "documentCount": 15, "instanceCount": 15},
                              {"entityTypeKey": "fathers_name",
                               "documentCount": 15, "instanceCount": 15},
                                               {"entityTypeKey": "name",
                                                "documentCount": 15,
                                                "instanceCount": 15},
                              {"entityTypeKey": "pan_id", "documentCount": 15,
                               "instanceCount": 15}]}},
                                {"type": "DATASET_SPLIT_TEST",
                                 "datasetStats": {"documentCount": 10,
                                 "statsEntries": [{"labelingStateKey":
                                                       "DOCUMENT_LABELED",
                                "documentCount": 10, "instanceCount": 10},
                                {"entityTypeKey": "dob", "documentCount": 10,
                                 "instanceCount": 10},
                                {"entityTypeKey": "fathers_name",
                                 "documentCount": 10, "instanceCount": 10},
                                {"entityTypeKey": "name", "documentCount": 10,
                                 "instanceCount": 10},
                                {"entityTypeKey": "pan_id", "documentCount": 10,
                                 "instanceCount": 10}]}},
                                {"type": "DATASET_SPLIT_UNASSIGNED",
                                 "datasetStats": {"documentCount": 18,
                                "statsEntries": [{"labelingStateKey":
                                                      "DOCUMENT_LABELED",
                                "documentCount": 18, "instanceCount": 18},
                                {"entityTypeKey": "dob", "documentCount": 18,
                                 "instanceCount": 19},
                                {"entityTypeKey": "fathers_name",
                                 "documentCount": 18, "instanceCount": 19},
                                 {"entityTypeKey": "name", "documentCount": 18,
                                  "instanceCount": 19},
                                {"entityTypeKey": "pan_id", "documentCount": 18,
                                 "instanceCount": 19}]}}]}

class TestCDC(unittest.TestCase, Var):
    maxDiff = None

    def __init__(self, *args, **kwargs) -> None:
        """ initiating  VarPath class methods """
        super().__init__(*args, **kwargs)
        Var.__init__(self)

    def test_get_url(self) -> None:
        url, _ = update_to_bq_cde.get_url(self.location, self.url_substring)
        url_actual = self.url_actual
        self.assertEqual(url, url_actual)

    @patch("update_to_bq_cde.requests.get")
    def test_get_train_test_size(self,mock_get_response) -> None:

        json_data = self.response_json
        status_code = 200    # for success
        mock_get_response.return_value = MockReponse(json_data, status_code)

        train_count, test_count = update_to_bq_cde.get_train_test_size(
            self.project_number,
            self.processor_id,
            self.location)
        train_count_actual = self.train_count_actual
        test_count_actual = self.test_count_actual
        self.assertEqual(train_count, train_count_actual)
        self.assertEqual(test_count, test_count_actual)

    def test_get_train_gcs_uri(self) -> None:
        gcs_uri = update_to_bq_cde.get_train_gcs_uri(self.project_number,
                                                 self.processor_id,
                                                 self.location)

        gcs_uri_actual = self.gcs_uri_actual
        self.assertEqual(gcs_uri, gcs_uri_actual)

    def test_get_main_dict_overall_dict(self) -> None:
        main_dict,\
        overall_main_dict = update_to_bq_cde.get_main_dict_overall_dict(
            self.class_dic, self.overall_dic)

        main_dict_actual = self.main_dict_actual
        overall_main_dict_actual = self.overall_main_dict_actual

        self.assertEqual(main_dict, main_dict_actual)
        self.assertEqual(overall_main_dict, overall_main_dict_actual)

    @patch("update_to_bq_cde.bigquery.Client")
    def test_add_modelmetrics_tobq(self, mock_bigquery_client) -> None:
        mock_bigquery_client().insert_rows.return_value = []
        mock_bigquery_client().get_table.return_value = None

        update_to_bq_cde.add_modelmetrics_tobq(self.model_name,
                                           self.job_id,
                                           self.processor_version_id,
                                           self.processor_id,
                                           self.processor_version_name,
                                           self.is_deployed,
                                           self.pipeline_name,
                                           self.region,
                                           self.ref_code_file_version,
                                           self.train_percent,
                                           self.train_size,
                                           self.test_size,
                                           self.timestamp,
                                           self.dataset_uri,
                                           self.overall_main_dict_actual,
                                           self.gcs_path_evaluation_csv,
                                           self.gcs_path_model,
                                           self.configuration,
                                           self.project_id,
                                           self.dataset_model,
                                           self.table_name_model)

    @patch("update_to_bq_cde.bigquery.Client")
    def test_add_classmetrics_tobq(self, mock_bigquery_client) -> None:
        mock_bigquery_client().insert_rows.return_value = []
        mock_bigquery_client().get_table.return_value = None

        update_to_bq_cde.add_classmetrics_tobq(self.main_dict_actual,
                                           self.model_name,
                                           self.job_id,
                                           self.processor_version_id,
                                           self.processor_id,
                                           self.processor_version_name,
                                           self.is_deployed,
                                           self.pipeline_name,
                                           self.region,
                                           self.doc_type,
                                           self.project_id,
                                           self.dataset_class,
                                           self.table_name_class)

    @patch("update_to_bq_cde.bigquery.Client")
    @patch("update_to_bq_cde.get_main_dict_overall_dict")
    @patch("update_to_bq_cde.add_modelmetrics_tobq")
    @patch("update_to_bq_cde.add_classmetrics_tobq")
    def test_write_metrics_to_bq(self, mock_add_classmetrics_tobq,
                                 mock_add_modelmetrics_tobq,
                                 mock_get_main_dict_overall_dict,
                                 mock_bigquery_client):
        mock_bigquery_client().insert_rows.return_value = []
        mock_bigquery_client().get_table.return_value = None

        mock_get_main_dict_overall_dict.return_value = self.main_dict_actual,\
                                                self.overall_main_dict_actual
        mock_add_classmetrics_tobq.return_value = None
        mock_add_modelmetrics_tobq.return_value = None

        update_to_bq_cde.write_metrics_to_bq(self.job_id,
                                         self.processor_id,
                                         self.project_number,
                                         self.ref_code_file_version,
                                         self.doc_type,
                                         self.is_deployed,
                                         self.configuration,
                                         self.project_id,
                                         self.region,
                                         self.timestamp,
                                         self.dataset_model,
                                         self.table_name_model,
                                         self.dataset_class,
                                         self.table_name_class,
                                         self.data_pipeline_root,
                                         self.model_name,
                                         self.pipeline_name,
                                         self.gcs_path_model,
                                         self.location,
                                         VersionName(),
                                         OverallMetrics(),
                                         ClassMetrics())
