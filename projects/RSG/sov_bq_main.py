#Import packages
import pandas_gbq
import pandas as pd
import numpy as np
from glob import glob
import os
import os.path
import io
import json

#import google cloud packages
from google.cloud import bigquery
from google.cloud import storage

# write to BQ table
def write_row_to_bq(main_df,project_id,table):
    print("******** WRITE TO BQ STARTS **********")
    pandas_gbq.to_gbq(main_df,table,project_id=project_id,if_exists="append")
    print("******** WRITE TO BQ ENDS **********")
     
   






















