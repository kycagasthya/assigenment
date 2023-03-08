# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

from docai.processor.v2.utils import helpers

obj = helpers.OnlinePred(
    project="india-dai-parsers",
    endpoint_id="3d9e2b41440368f8",
    location="us",
    request_id="123",
    page_id="456")

path = "/home/deepak/api/tc001.png"

with open(path, "rb")as fp:
    image_data = fp.read()
pred = obj.predict_cde(image_data, doc_type="aadhar")

print(pred)
