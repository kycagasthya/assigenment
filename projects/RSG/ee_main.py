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
processor_id = config['processor_id']



def main(gcs_input_uri, doc_type, doc_uuid):
    """
    1. Run pre-processing of the input document
    2. Check and call the EE code as per doc_type
    3. Return final json
    """
    input_bucket = gcs_input_uri.split('/')[2]
    file_path = "/".join(gcs_input_uri.split("/")[3:])
    logger_ee = ""
    #doc_type = doc_type.lower().replace(' ','')
    try:
        doc, page_orientations,results = fp_split_update.pre_process('/tmp/'+doc_uuid+'.pdf', file_path, input_bucket, 
                             project_id, location, processor_id)

        if 'error' in doc:
            return doc,'failed', 404
            
        if doc_type == "acord":
            # doc_type_final = "acord"
            import acord_125
            
            resp, status, code = acord_125.acord_main(doc, doc_uuid,results)
            if status == 'failed':
                return resp , status, code
            
        elif doc_type == "binder":
            # doc_type_final = "binder"
            import binder
            
            resp, status, code = binder.binder_main(doc, doc_uuid, results)
            if status == 'failed':
                return resp , status, code
            
        elif doc_type == "policy":
            # doc_type_final = "policy"
            import policy
            
            resp, status, code = policy.policy_main(doc, doc_uuid, results)
            if status == 'failed':
                return resp , status, code
            
        
        else:
            return {"error": "Invalid doc type: " + str(doc_type)}, 'failed', 404


        if 'error' not in resp:
            
            #saving the response into csv
            #resp.to_csv("sample_acord_csv_1.csv", index = False)
            resp.to_csv("sample_binder_csv_1.csv", index = False)
            # resp.to_csv("sample_policy_csv_1.csv", index = False)
        
        return resp, status, code

    except:        
        return {"error": "Entity Extraction failed due to: " + str(traceback.format_exc())}, 'failed', 404

        


#-------Running individual files----------
# print(main("gs://data_from-rsg/Application/CPS3958922 Acord Application.pdf", "acord","CPS3958922 Acord Application"))

# print(main("gs://mgi-dev-consumer-kyc-images-outputs/CPS3958922 Binder.pdf", "binder","CPS3958922 Binder"))

# print(main("gs://mgi-dev-consumer-kyc-images-outputs/CPS3958922 Policy.pdf", "policy","CPS3958922 Policy"))
