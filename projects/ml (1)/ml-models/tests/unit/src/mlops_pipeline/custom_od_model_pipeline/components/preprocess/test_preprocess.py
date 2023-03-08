# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================
import sys
import unittest
from unittest import mock
from unittest.mock  import patch
import xml.etree.ElementTree as ET
sys.path.insert(
    0, "src/mlops_pipeline/custom_od_model_pipeline/components/preprocess/src")
mocked_tf = mock.MagicMock()
sys.modules["tensorflow"] = mocked_tf
sys.modules["tensorflow.compat.v1"] = mocked_tf
import preprocess
from preprocess_utils import delete_blob, file_exist
from os.path import dirname, abspath
current_dir = abspath(dirname(__file__))


class TrainTestCount:
    metadata = {"test_size":"","train_size":""}

class OutputTrain:
    uri = "gs://asia/od-mlops/preprocess_data/scf_data/test"

class OutputValidation:
    uri = "gs://asia/od-mlops/preprocess_data/scf_data/test"

class DummyBucket:
    def list_blobs(self, prefix=None):
        prefix =  Blob("gs://bucket/dummy2.xml")
        return [
            Blob("standard_preprocessed_images_.csv"),
            Blob("gs://bucket/dummy1.xml"), prefix]

class DummyWriter:
    def write(self, dummy):
        dummy = True
        return dummy

    def close(self):
        pass

class TFExample:
    def SerializeToString(self):
        pass

class Blob:
    def __init__(self, name):
        self.name = name

    def blob(self,dummy):
        dummy = Blob("dummy")
        return dummy

    def delete(self):
        pass

    def exists(self, dummy):
        dummy = True
        return dummy

class Variable:
    data_path = "gs://asia/od-mlops/preprocess_data/scf_data/test"
    label_path = "gs://asia/od-mlops/preprocess_data/label_map_class.pbtxt"
    out_path = "gs://asia/od-mlops/preprocess_data/scf_data/out"
    root = "gs://dummyroot/20220529171616"
    xml_path = f"{current_dir}/test_data/sample.xml"
    train_test_count = TrainTestCount()
    output_train = OutputTrain()
    output_validation = OutputValidation
    json_path = "test.json"
    dummy_df = {"file_name":"gs://bucket/ummy1.xml gs://bucket/dummy2.xml"}



class TestPreprocess(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @patch("preprocess.storage.Client")
    @patch("preprocess.gcsfs.GCSFileSystem")
    @patch("preprocess.pd")
    @patch("preprocess.list")
    @patch("preprocess.delete_blob")
    @patch("preprocess.ET.parse")
    def test_xml_to_csv(
        self, mock_et, mock_delete, mock_list,
        mock_pandas,mock_gcs_file_system, mock_storage):
        mock_storage().get_bucket.return_value = DummyBucket()
        mock_pandas.read_csv.return_value = Variable.dummy_df
        mock_list.return_value = ["dummy1", "dummy2"]
        mock_delete.return_value = True
        fp = open(Variable.xml_path, "r")
        mock_gcs_file_system().open.return_value = fp
        mock_et.return_value = ET.parse(fp)
        status, _ = preprocess.xml_to_csv(Variable.data_path, "")
        self.assertEqual(status, True)

    @patch("preprocess.storage.Client")
    @patch("preprocess.pd")
    @patch("preprocess.list")
    def test_xml_to_csv_fail(
        self, mock_list,
        mock_pandas, mock_storage):
        mock_storage().get_bucket.return_value = DummyBucket()
        mock_pandas.read_csv.return_value = Variable.dummy_df
        mock_list.return_value = ["test", "test"]
        status, _ = preprocess.xml_to_csv(Variable.data_path, "")
        self.assertEqual(status, False)

    @patch("preprocess.file_exist")
    @patch("preprocess.label_map_util")
    @patch("preprocess.storage.Client")
    @patch("preprocess.gcsfs.GCSFileSystem")
    @patch("preprocess.dataset_util.create_tf_example")
    @patch("preprocess.pd")
    @patch("preprocess.list")
    @patch("preprocess.delete_blob")
    @patch("preprocess.ET.parse")
    def test_main(
            self, mock_et, mock_delete, mock_list, mock_pandas,
            mock_create_tf_example, mock_gcs_file_system, mock_storage,
            mock_label_map_util, mock_file_exist):#, mock_writer):
        mocked_tf.python_io.TFRecordWriter.return_value = DummyWriter()
        mock_file_exist().return_value = True
        mock_label_map_util.load_labelmap.return_value = "dummy"
        mock_label_map_util.get_label_map_dict.return_value = {}
        mock_storage().get_bucket.return_value = DummyBucket()
        mock_gcs_file_system().open.return_value = open(Variable.xml_path, "r")
        mock_create_tf_example.return_value = TFExample()
        mock_pandas.read_csv.return_value = Variable.dummy_df
        mock_list.return_value = ["dummy1", "dummy2"]
        mock_delete.return_value = True
        mock_gcs_file_system().open.return_value = open(Variable.xml_path, "r")
        mock_et.return_value = ET.parse(open(Variable.xml_path, "r"))
        status, count = preprocess.main(
            Variable.data_path, Variable.label_path, Variable.out_path, "")
        self.assertEqual(status, True)
        self.assertEqual(count, 0)

    @patch("preprocess.main")
    @patch("preprocess.gcsfs.GCSFileSystem")
    def test_preprocess(self, mock_gcs_file_system, mock_main):
        mock_main.return_value = (True, "10")
        mock_gcs_file_system().open.return_value = open(Variable.json_path, "w")
        preprocess.preprocess(
            Variable.data_path, Variable.data_path, Variable.label_path,
            Variable.root,Variable.output_train, Variable.output_validation)

    @patch("preprocess.main")
    @patch("preprocess.gcsfs.GCSFileSystem")
    def test_preprocess_fail(self, mock_gcs_file_system, mock_main):
        try:
            mock_main.return_value = (False, "10")
            mock_gcs_file_system().open.return_value = open(
                Variable.json_path, "w")
            preprocess.preprocess(
                Variable.data_path, Variable.data_path,
                Variable.label_path, Variable.root,
                Variable.output_train, Variable.output_validation)
        except Exception as e:
            self.assertEqual(str(e), "Preprocessing component failed")

    @patch("preprocess_utils.storage.Client")
    def test_delete_blob(self, mock_storage_client):
        mock_storage_client().bucket.return_value = Blob("dummy")
        delete_blob("a", "b")

    @patch("preprocess_utils.storage")
    def test_file_exist(self, mock_storage):
        mock_storage.Client().bucket.return_value = "dummy_bucket"
        mock_storage.Blob.return_value = Blob("dummy")
        stat = file_exist("gs://bucket/file")
        self.assertEqual(True, stat)
