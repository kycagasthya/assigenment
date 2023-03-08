# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================
from os.path import dirname, abspath
current_dir = abspath(dirname(__file__))

metric_calc_actual = [0,1,1,0,0]
metric_calc_pred = [0,1,0,0,1]
metric_cal_result = (2, 1, 1, 1, 0.5, 0.5, 0.5)
bucket_name = "dummy_bucket"
prefix = "dummy_folder"
gs_path = "gs://dummy_bucket/dummy_folder"
file_list = ["gs://dummy_bucket/dummy.jpg", "gs://dummy_bucket/dummy.jpg"]
threshold = 0.3
test_data_path = "dummy"
dummy_filepaths = [
    "one_signature_1.jpg","two_signature_1.jpg","three_signature_1.jpg"]
out_csv_path = f"{current_dir}/test_data"
model_path = f"{current_dir}/test_data/bytes_model"
cdc_json_path = \
f"{current_dir}/test_data/SCF3-4_12226353-65c8-590c-bce1-d78536316d8b_0.json"
key_words_actual = ("CUSTOMER", "DECLARATION", "BRANCH", "ONLY")
img_path_scf = f"{current_dir}/test_data/SCF.png"
applicants_key_actual = ("Primary", "Applicant", "Holder", "Joint")
bounding_box_dict = {
    "displayNames": ["signature", "signature", "signature"],
    "bboxes": [
        [0.11654666066169739, 0.24870741367340088,
         0.7035818696022034, 0.7329686284065247],
        [0.6744846701622009, 0.8365553021430969,
         0.882803201675415, 0.9141350984573364],
        [0.3764748275279999, 0.5482677221298218,
         0.8801876306533813, 0.9099823236465454]],
    "confidence": [
        0.444252610206604, 0.38338935375213623,
        0.32991689443588257]}
extract_result = (True, False, False, 0.444252610206604, 0, 0)
combine_list = [
                    {"x": 500, "y": 1074},
                    {"x": 609, "y": 1075},
                    {"x": 609, "y": 1110},
                    {"x": 500, "y": 1109},
                    {"x": 619, "y": 1074},
                    {"x": 760, "y": 1075},
                    {"x": 760, "y": 1110},
                    {"x": 619, "y": 1109},
                ]
roi_coordinates_actual = ((500, 1074), (760, 1110))
