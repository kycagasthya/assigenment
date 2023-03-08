# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

from docai.imageproc.docsplit.utils import helpers as docsplit_helper
from docai.imageproc.pre_processor.utils import helpers as pre_proc_helper

gcs_uri = "gs://icici-ia-docai-img-prep/raw-pages/crm/2022/Test Raw \
    data/Adhar/Template1/tc010b.png"
doc_split = docsplit_helper.DocSplitting(
    gcs_uri=gcs_uri, request_id="123", page_id="987"
)
num_pages, list_img, mimetype = doc_split.run()
file_bytes = list_img[0]
operations = pre_proc_helper.ImageOperation(
    file_bytes, request_id="123", page_id="987")
content, dpi_value, pixel_flag = operations.preprocess_bytes()
response = operations.bytes_detect_text(content)
