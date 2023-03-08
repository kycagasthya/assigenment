from google.cloud import storage
import os
import numpy as np
import traceback
import pandas as pd

def read_files(bucket_name, file_name, project_id):
    print("******** READ_FILES FUNCTION STARTS **********")
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    data_bytes = blob.download_as_bytes(client=client)
    list_df = []
    filename = os.path.basename(blob.name)
    cols = ['Policy_no','Bldg_Num', 'Location_Name', 'Street_Address','City', \
            'State_Code', 'Zip', 'County', 'Num_Of_Blds',
            'ISO_construction_type', 'Num_Of_Stories',\
            'Year_Built', 'Real_Property_Value','Personal_Property_Value',\
            'Business_Income', 'Num_Of_Units', 'Square_Footage', "Percent_Sprinklered",\
            'ISO_Protection_Classification']

    try:
        df = pd.read_excel(data_bytes, sheet_name='SOV-APP', header=11)
        df['Policy_no'] = filename.split(" ")[0]

        # Renaming columns
        df.rename(columns = {'* Bldg No.':'Bldg_Num', 'Location Name': 'Location_Name', \
                             '*Street Address':'Street_Address','*City':'City', \
                             '*State Code': 'State_Code', '*Zip':'Zip', 'County':'County', \
                             '*# of Bldgs': 'Num_Of_Blds','*ISO Const': \
                             'ISO_construction_type', '*# of Stories': 'Num_Of_Stories', \
                             '*Orig Year Built':'Year_Built','*Real Property Value ($)': \
                             'Real_Property_Value', 'Personal Property Value ($) ': \
                             'Personal_Property_Value', 'BI/Rental Income ($)': \
                             'Business_Income', '*# of Units':'Num_Of_Units', \
                             '*Square Footage':'Square_Footage', \
                             'Percent Sprinklered': "Percent_Sprinklered", 'ISO Prot Class':\
                             'ISO_Protection_Classification'}, inplace = True)

        sample_df = df[[*cols]]

        # Creating one variable who has all columns except 'Bldg_Num'
        temp = [col for col in sample_df.columns if col!='Bldg_Num']

        # Drop those rows whose all columns have Null value except Bldg_Num
        sample_df.dropna(subset=temp,how='all',inplace=True)
        
        #print(sample_df.columns)
        sample_df.dropna(how = 'any', thresh = 3, inplace = True)
        
        # Replacing 'NaN' with ''
        sample_df.replace(np.NaN, 'NULL', inplace = True)
        list_df.append(sample_df)
        sample_df.columns=sample_df.columns.str.upper()
        print("Name of the Excel Executed: ", filename)
    except:
        print(str(traceback.format_exc()),"********** INSIDE SOV EXCEPT BLOCK **********")
        print('Name of Corrputed file is:',filename)

    # Concating all four files which are in list
    df = pd.concat(list_df) 
    
    #Converting Datatype
    df = df.applymap(lambda x:str(x))
    print("******** READ_FILES FUNCTION ENDS **********")
    return df
