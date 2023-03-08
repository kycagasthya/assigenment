import os
from flask import Flask, request
from sov import read_files
from sov_bq_main import write_row_to_bq
#from config import PROJECT_ID, table
import time
from ee_main import main
import fp_split_update
import json
import pandas as pd
import traceback
import proto


#reading config file for inputs
with open('config_ee.json') as f:
    config = json.load(f)

project_id= config['project_id']
location = config['location']
table= config['table']
processor_id = config['processor_id']

app = Flask(__name__)
@app.route("/")
def hello_world():
    """
    Takes the request as a uploaded file
    Process it to the extraction pipeline and inserts data into BQ
    """
    print('************ CLOUD RUN STARTS ************')
    file_name = request.headers['file_name']
    bucket_name = request.headers['bucket_name'] #rsg-project
    rev_file_name = file_name.split('/')[-1]
    doc_type = file_name.split('/')[-2]
    gcs_uri = f"gs://{bucket_name}/{doc_type}/{rev_file_name}"
    print(gcs_uri,'************ GCS_URI ************')
    print(rev_file_name,'************ REVISED_FILE_NAME ************')
    print(doc_type,'************ DOCUMENT TYPE ************')
    print(file_name,'************ FILE_NAME ************')
    uuid = rev_file_name.split(".")[0]
    print(uuid,'************ UUID ************')
    if rev_file_name.lower().endswith(('xls','xlsx','xlsb')):
        main_df = read_files(bucket_name, file_name, project_id)
        time.sleep(2)
        write_row_to_bq(main_df, project_id, table)
    else:
        doc_type = doc_type.lower()
        res, status, code = main(gcs_uri, doc_type, uuid)
        if code == 500:
            print("Cloud Run failed due to:", res)
        else:
            print(res,'******** OUTPUT RESPONSE ************')    
    

    print('************ CLOUD RUN COMPLETES ************')
    return "successfull",200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    