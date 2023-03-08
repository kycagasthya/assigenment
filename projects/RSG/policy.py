"""Import packages"""
import re
import traceback
from datetime import datetime
import pandas as pd
import numpy as np
import json
from google.cloud import storage

BUCKET_NAME = 'rsg-data-tagging'
# PROJECT_ID = "q-gcp-6508-rsg-docai-22-01"
# TABLE = "testdataset.policy_2102"
with open('config_ee.json') as f:
    config = json.load(f)

PROJECT_ID= config['project_id']
TABLE = config['table_policy_rsg']
def policy_entity_extraction(document, filename, doc_obj_list):
    """Policy related 19 entity extraction"""    
    def _get_text(elem, doc):
        """Convert text offset indexes into text snippets."""
        response = ""
        """If a text segment spans several lines, it will
           be stored in different text segments."""
        for segment in elem.text_anchor.text_segments:
            start_index = segment.start_index
            end_index = segment.end_index
            response += doc.text[start_index:end_index]
        return response
    for doc in doc_obj_list:
        for page in doc.pages:
            #print("page number", page.page_number)
            for _, table in enumerate(page.tables):
                for _, row in enumerate(table.header_rows):
                    cells = "".join([_get_text(cell.layout, doc) for cell in row.cells])
                    if "State, Zip Code)" and "Occupancy" in cells: #
                        for _, row in enumerate(table.body_rows):
                            cells1 = [(_get_text(cell.layout, doc)).strip('\n') for cell in row.cells]
                            if len(cells1) > 4:
                                #print(">4", cells1)
                                cells_mid = []
                                if len(cells1[0]) ==0:
                                    cells_mid.append('NULL')
                                    cells1[2]= ' '.join(cells1[2:-1])
                                    if cells1[1].isdigit():
                                        cells_mid.append(cells1[1])
                                    else:
                                        cells_mid.append('NULL')
                                    cells_mid.append(cells1[2])
                                    cells_mid.append(cells1[-1])
                                    loc_values.append(cells_mid)
                                    #print("loc_values", loc_values)
                                elif len(cells1[0]) == 3 and cells1[1].isdigit():
                                    cells1[2]= ' '.join(cells1[2:-1])
                                    if cells1[0][0].isdigit():
                                        cells_mid.append(cells1[0][0])
                                    cells_mid.append(cells1[1])
                                    cells_mid.append(cells1[2])
                                    cells_mid.append(cells1[-1])
                                    loc_values.append(cells_mid)
                                elif len(cells1[0])>1 and '\n' in cells1[0]:
                                    n1, n2 = cells1[0].split('\n')
                                    cells_mid.append(n1)
                                    cells_mid.append(n2)
                                    cells1[2]= ' '.join(cells1[1:-1])
                                    cells_mid.append(cells1[2])
                                    cells_mid.append(cells1[-1])
                                    loc_values.append(cells_mid)
                                else:
                                    cells1[2]= ' '.join(cells1[2:-1])
                                    if cells1[0].isdigit():
                                        cells_mid.append(cells1[0])
                                    cells_mid.append(cells1[1])
                                    cells_mid.append(cells1[2])
                                    cells_mid.append(cells1[-1])
                                    loc_values.append(cells_mid)
                                    #print("loc_values", loc_values)
                            elif len(cells1) == 4:
                                #print("==4", cells1)
                                cells_m2 = []
                                if len(cells1[0]) < 5:
                                    cells_m2.append(cells1[0])
                                    if len(cells1[1]) < 5:
                                        cells_m2.append(cells1[1])
                                    cells_m2.append(cells1[2])
                                    cells_m2.append(cells1[3])
                                    loc_values.append(cells_m2)
                                    #print("loc_values", loc_values)
                                elif len(cells1[0]) < 5:
                                    cells_m2.append(cells1[0])
                                    if len(cells1[1]) > 5:
                                        cells_m2.append("NULL")
                                    cells_m2.append(cells1[1])
                                    cells_m2.append(cells1[2])
                                    loc_values.append(cells_m2)
                                    #print("loc_values", loc_values)
                            else:
                                #print("<4", cells1)
                                #print("else cells1", cells1)
                                cells_m = []
                                if cells1[0].isdigit and len(cells1[0])<3:
                                    cells_m.append(cells1[0])
                                    if len(cells1[1]) > 3 and '\n' in cells1[1][0:5]:
                                        cells_m.append(cells1[1][0])
                                        cells_m.append(cells1[1])
                                        cells_m.append(cells1[2])
                                        loc_values.append(cells_m)
                                    else:
                                        cells_m.append("NULL")
                                        cells_m.append(cells1[1])
                                        cells_m.append(cells1[2])
                                        loc_values.append(cells_m)                                        
                 #                       print("loc_values", loc_values)
                                elif len(cells1[0])==3 and not cells1[0].isdigit:
                                    cells_m.append(cells1[0].split(' ')[0])
                                    cells_m.append(cells1[0].split(' ')[1])
                                    if len(cells1[1]) > 2:
                                        cells_m.append(cells1[1])
                                        cells_m.append(cells1[2])
                                        loc_values.append(cells_m)
                                elif len(cells1[0])>1 and '\n' in cells1[0]:
                                    n1, n2 = cells1[0].split('\n')
                                    cells_m.append(n1)
                                    cells_m.append(n2)
                                    if len(cells1[1]) > 2:
                                        cells_m.append(cells1[1])
                                        cells_m.append(cells1[2])
                                        loc_values.append(cells_m)
                    #print("loc_values", loc_values)
                    if "Coins" in cells or "Limit of\nInsurance" in cells or "\nCauses of Loss" in cells:
                        for row in table.body_rows:
                            cells2 = [(_get_text(cell.layout, doc)).strip('\n') for cell in row.cells]
                            if len(cells2[0]) < 3 and len(cells2) == 6 and \
                            cells2.count('') < 3 and len(cells2[2]) >6:
                                cov_values.append(cells2)
                    if 'Premises' and 'Protective Safeguards' and 'Symbols Applicable' in cells:
                        for row in table.body_rows:
                            cells3 = [(_get_text(cell.layout, doc)).strip('\n') for cell in row.cells]
                            #print(cells3)
                            if len(cells3) < 4 and cells3[0].isdigit():
                                iso_values.append(cells3)
    #print("Initial response",loc_values, cov_values, iso_values)
    return loc_values, cov_values, iso_values
def policyno_eff_date_insured(texts):
    """Policy number, eff date and insured details extracted using REGEX"""
    for matchtext in re.findall(r'(?<=Policy Number:).*?(?=Agent Number:)', texts):
        pol_eff_date_insured = matchtext.split()
        if 'Effective' in pol_eff_date_insured:
            pol = matchtext.split("Effective")[0]
            if len(pol) <13 and any(d in pol for d in'0123456789'):
                policy = pol.split(' ')[1]
                policyno = policy
        search = 'Effective Date'
        if 'Date:' in pol_eff_date_insured:
            try:
                eff_d = matchtext.split("Date:")[1]
                eff_date = eff_d.split()[0]
                datetime.strptime(eff_date, '%m/%d/%Y')
            except ValueError:
                eff_index = [i for i, string in enumerate(texts) if search in string]
                eff_date = texts[eff_index[0] + 1]
            except IndexError:
                eff_date = "NULL"
        try:
            insured_substring = ['Effective', 'Date:', policyno, eff_date, '(12:01 A.M. Standard Time)' ,'Named', 'Insured:']
            test_str = matchtext
            for sub in insured_substring:
                test_str = test_str.replace(sub, '')
            insured = " ".join(test_str.split())
        except Exception as _:
            if "Insured:" in pol_eff_date_insured:
                insured = matchtext.split("Insured:")[1]
    return policyno, eff_date, insured
def find_zip(str):
    """Regex to extract 5 digit Zip code from Address"""
    #print("zipcode",str)
    try:
        #print("Trying zipcode", str)
        zip_c = re.findall(r'(\d{5}\-?\d{0,4})', str)
        zip_code = [item for item in zip_c if len(item)==5]
        #print("zip_code values", zip_code)
    except Exception as _:
        zip_code = ['NULL']
    #print("final zip",zip_code)
    #print(zip_code[-1])
    return zip_code[-1]
def find_city(str):
    """Regex for extracting city from Address"""
    try:
        city_re = re.findall("[A-Za-z]+", str)
        #print("city_re", city_re)
        if len(city_re[-2]) ==5 and city_re[-2] == 'MIAMI' or city_re[-2] == 'TAMPA':
            city = city_re[-2]
        elif len(city_re[-2]) > 5:
            city = city_re[-2]
        else:
            city = city_re[-3] + ' ' +city_re[-2]
    except Exception as _:
        city = ['NULL']
    return city
def find_state(str):
    """Regex for extracting State from Address"""
    try:
        state = re.findall(r'([A-Z][A-Z])', str)
    except Exception as _:
        state = ['NULL']
    return state[-1]
def try_ext(addres, cit):
    """Extracting street address"""
    idx = addres.find(cit)
    new_string = addres[0:idx]
    return new_string
def iso_table_creation(filename, iso_values, doc):
    """ISO protection class extraction"""
    df_iso = pd.DataFrame()
    try:
        iso_list = ['BR-1', 'BR-4']
        if len(iso_values) >0:
            df_iso = pd.DataFrame(iso_values, columns = ['premno', 'bldgno', 'iso_protection_class'])
            df_iso['filename'] = filename
        else:
            df_iso['filename'] = filename
        df_iso.drop(df_iso.index[df_iso['iso_protection_class'].isin(iso_list)], inplace = True)
        df_iso.drop_duplicates(keep='last', inplace = True)
        df_iso.to_csv("ISO table.csv", index = False)
    except Exception as _:
        df_iso['filename'] = filename
    return df_iso
def location_table_creation(filename, cells_loc_values, doc, texts):
    """Location related details extraction"""
    df_loc = pd.DataFrame()
    duplicates = ['See Liability\nDec(s)', 'Property in the\nOpen', 'Property in the\nOpen\nProperty in the\nOpen']
    #filname = filename
    #print("LOC filename", filename)
    #print("Location table", cells_loc_values)
    #print("Location table filename", filename)
    if len(cells_loc_values) > 0:
        #print(len(cells_loc_values))
        try:
            df_loc = pd.DataFrame(cells_loc_values, columns = ['premno', 'bldgno', 'street_address', 'occupancy_type'])
            df_loc.drop(df_loc.index[df_loc['occupancy_type'].isin(duplicates)], inplace = True)
            df_loc = df_loc.dropna(subset=['occupancy_type'])
            df_loc.to_csv("Location_put_in_df.csv")
            df_loc['filename'] = filename
            #print("With filename")
            print("df_loc", df_loc)
            df_loc['zipcode'] = df_loc['street_address'].map(find_zip)
            #print("1 zipcode")
            df_loc['city'] = df_loc['street_address'].map(find_city)
            #print("2 city")
            df_loc['state'] = df_loc['street_address'].map(find_state)
            #print("3 state")
            df_loc['street_address'] = [try_ext(a, c) for a , c in zip(df_loc.street_address, df_loc.city)]
            #print("4 street_address")
            df_loc.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
            cells_loc_values.clear()
            df_loc['premno'].fillna(method='backfill', inplace=True)
            df_loc['bldgno'].fillna(method='backfill', inplace=True)
            df_loc.dropna(axis = 0, subset = ['premno', 'bldgno'], how = 'all', inplace = True)
            df_loc.fillna('NULL', inplace=True)
            df_loc = df_loc.drop_duplicates(['filename','premno', 'bldgno'],keep= 'last')
            #print("df_loc final", df_loc)
        except Exception as _:
            #print("loc exception", _)
            df_loc = pd.DataFrame()
            df_loc['filename'] = filename
    else:
        df_loc = pd.DataFrame()
        df_loc['filename'] = filename
    #print("DF_loc final", df_loc)
    df_loc.to_csv("Location table1.csv", index = False)
    return df_loc
def coverage_table_creation(filename, cov_values, doc, texts):
    """Coverage details extraction"""
    df_cov = pd.DataFrame()
    df_cov_final = pd.DataFrame()
    #filname = filename
    if len(cov_values) > 0:
        #try:
        df_cov = pd.DataFrame(cov_values, columns = ['premno', 'bldgno', 'coverage', 'limitofinsurance', 'causesofloss', 'coins'])
        df_cov['filename'] = filename
        cov_list = df_cov['coverage'].unique().tolist()
        df_cov_mid = pd.get_dummies(df_cov, columns = ['coverage'], prefix='', prefix_sep='')
        for i in cov_list:
            df_cov_mid[i] = np.where(df_cov_mid[i]==1, df_cov_mid['limitofinsurance'], np.nan)   
        cov_cols = ['filename', 'premno', 'bldgno', 'causesofloss', 'coins', 'BUILDING', 'BUSINESS PERSONAL PROPERTY', 'BUSINESS INCOME WITH EXTRA EXPENSE', 'PIO PROPERTY IN THE OPEN','TENANT IMPROVEMENTS AND BETTERMENTS']
        df_cov_f = df_cov_mid[df_cov_mid.columns.intersection(cov_cols)]
        df_cov_final = df_cov_f.fillna(np.nan).groupby(['premno', 'bldgno'], as_index=False).first()
        df_cov_final.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
        int_cols = ['BUILDING','BUSINESS PERSONAL PROPERTY','PIO PROPERTY IN THE OPEN', 'TENANT IMPROVEMENTS AND BETTERMENTS', 'BUSINESS INCOME WITH EXTRA EXPENSE']
        for col in int_cols:
            if col in df_cov_final.columns:
                df_cov_final[col] = df_cov_final[col].str.replace(',', '').str.replace('$', '').astype(float)     
        sum_cols = ['PIO PROPERTY IN THE OPEN', 'TENANT IMPROVEMENTS AND BETTERMENTS']
        df_cov_final['OUTDOOR EXPENSE'] = df_cov_final.reindex(sum_cols, axis=1).sum(axis=1)
        sum_cols = ['BUILDING','BUSINESS PERSONAL PROPERTY','BUSINESS INCOME WITH EXTRA EXPENSE','PIO PROPERTY IN THE OPEN', 'TENANT IMPROVEMENTS AND BETTERMENTS']
        df_cov_final['Total_TIV'] = df_cov_final.reindex(sum_cols, axis=1).sum(axis=1)
        df_cov_final.dropna(axis = 0, subset = ['premno', 'bldgno'], how = 'all', inplace = True)
        cov_values.clear()
        cov_list.clear()
        # except Exception as _:
        #     df_cov_final['filename'] = filname
            #print(str(traceback.format_exc()),"********** INSIDE Coverage **********")  
    else:
        df_cov_final['filename'] = filename
    #print("1. df_cov_final", df_cov_final)
    df_cov_final.to_csv("Coverage table1.csv", index = False)
    return df_cov_final
def coverage_table_2_creation(document, filename, doc_obj_list):
    """COVERAGE detailas with year built and num stories"""
    cov2 =[] = pd.DataFrame()
    df_cov_2_mid = pd.DataFrame()
    df_cov_2 = pd.DataFrame(columns = ['filename','premno', 'bldgno', 'construction', 'original_year_built','num_stories'])
    for doc in doc_obj_list:
        texts = " ".join(doc.text.split('\n'))
        if "COMMERCIAL PROPERTY COVERAGE PART" and "SUPPLEMENTAL DECLARATIONS" in texts:
            for matchedtext in re.findall(r'(?<=Loss Coins.).*?(?=Replacement Cost:)', texts):
                const = matchedtext.split()
                #print("Matchedtext", const)
                if "$" and "Construction:" in const:
                    try:
                        const_mid = matchedtext.split("Construction:")[0]
                        con_f =  const_mid.split("$")[0]
                        number_list = re.findall('\d+', con_f)
                        if len(number_list) == 2:
                            premno, bldgno = number_list[0], number_list[1]
                        elif len(number_list) == 1:
                            premno, bldgno = number_list[0], 'NULL'
                        else:
                            premno, bldgno = np.nan, np.nan
                    except Exception as _:
                        premno, bldgno = np.nan, np.nan
                if "Construction:" in const:
                    try:
                        const_mid = matchedtext.split("Construction:")[1]
                        const_f = const_mid.split("Agreed")[0]
                        construction = const_f[:-1]
                    except Exception as _:
                        construction = 'NULL'
                if "Built:" in const:
                    try:
                        year_mid = matchedtext.split("Built:")[1]
                        print("year_mid", year_mid)
                        yr_num_list = re.findall('\d+', year_mid)
                        #print("yr_num_list", yr_num_list)
                        #print("year: from yr_num_list", yr_num_list[0])
                        if len(yr_num_list) == 2:
                            original_year_built, num_stories = yr_num_list[0], yr_num_list[1]
                        elif len(yr_num_list) == 1:
                            original_year_built, num_stories = yr_num_list[0], 'NULL'
                        else:
                            original_year_built, num_stories = 'NULL', 'NULL'
                        print("original_year_built, num_stories", original_year_built, num_stories)
                    except Exception as _:
                        print("year built exception", _)
                        original_year_built, num_stories = 'NULL', 'NULL'
                cov2 = [filename, premno, bldgno, construction, original_year_built, num_stories]
                df_cov_2_mid = df_cov_2_mid.append(pd.Series(cov2, index = df_cov_2.columns), ignore_index=True)
                df_cov_2_mid.dropna(axis = 0, subset = ['premno', 'bldgno'], how = 'all', inplace = True)
        df_cov_2 = pd.concat([df_cov_2, df_cov_2_mid], axis=0).reset_index(drop=True)
    df_cov_2.drop_duplicates(['filename','premno', 'bldgno'],keep= 'last', inplace = True) # 'num_stories'
    df_cov_2.to_csv("Coverage 2 table.csv", index = False)
    return df_cov_2
def merge_tables(df_loc, df_cov, df_cov_2, df_iso):
    """Merging tables"""
    policy_df = pd.DataFrame()
    dfcov = pd.DataFrame()
    df1 = pd.DataFrame()
    try:
        if len(df_cov) > 0 and len(df_cov_2) > 0:
            dfcov = pd.merge(df_cov, df_cov_2, on=['premno', 'bldgno', 'filename'], how='inner')
        elif len(df_cov) > 0 and len(df_cov_2) ==0:
            dfcov = df_cov
        elif len(df_cov) == 0 and len(df_cov_2) >0:
            dfcov = df_cov
    except Exception as _:
        dfcov = pd.merge(df_cov, df_cov_2, on=['filename'], how='inner')
    print("merged cov1, cov2", dfcov)
    try:
        if len(df_loc) > 0 and len(dfcov) > 0:
            df1 = pd.merge(df_loc, dfcov, on=['premno', 'bldgno', 'filename'], how='inner')
        elif len(df_loc) > 0 and len(dfcov) ==0:
            df1 = df_loc
        elif len(df_loc) == 0 and len(dfcov) >0:
            df1 = dfcov
    except Exception as _:
        df1 = pd.merge(df_loc, dfcov, on=['filename'], how='inner')
    print("Merged loc, cov1, cov2", df1)
    try:
        if len(df1)>0 and len(df_iso) >0:
            policy_df = pd.merge(df1, df_iso, on=['premno', 'bldgno', 'filename'], how='left')
            policy_df.fillna('NULL', inplace = True)
        elif len(df1)>0 and len(df_iso) ==0:
            policy_df = df1
        elif len(df1)==0 and len(df_iso) >0:
            policy_df = df_iso
    except Exception as _:
        policy_df = pd.merge(df1, df_iso, on=['filename'], how='inner')
    policy_df.fillna('NULL', inplace = True)
    policy_df.to_csv("Full dataframe.csv", index = False)
    return policy_df
def policy_main(document, filename, doc_obj_list):
    """Main function to call other functions"""
    global loc_values
    global cov_values
    global iso_values
    loc_values, cov_values, iso_values = [], [], []
    docum = document.text.split('\n')
    texts = " ".join(document.text.split('\n'))
    df_policy = pd.DataFrame()
    df_policy_final = pd.DataFrame()
    try:
        try:
            loc_values, cov_values, iso_values =  policy_entity_extraction(document, filename, doc_obj_list)
            policyno, eff_date, insured = policyno_eff_date_insured(texts)
            df_loc = location_table_creation(filename, loc_values, docum, texts)
            df_cov = coverage_table_creation(filename, cov_values, docum, texts) 
            df_iso = iso_table_creation(filename, iso_values, docum)
            df_cov_2 = coverage_table_2_creation(document, filename, doc_obj_list)
            df_policy = merge_tables(df_loc, df_cov, df_cov_2, df_iso)
            df_policy['policyno'] = policyno
            df_policy['eff_date'] = eff_date
            df_policy['insured'] = insured
            col_dict = {'filename': 'FILENAME',
                'policyno': 'POLICY_NO', #POLICY_POLICY_NO
                'eff_date': 'POLICY_EFF_DATE',
                'insured':'INSURED',
                'premno':'POLICY_PREMNO',
                'bldgno':'POLICY_BLDGNO',
                'street_address':'POLICY_STREET_ADDRESS',
                'city':'POLICY_CITY',
                'state':'POLICY_STATE',
                'zipcode':'POLICY_ZIP',
                'construction':'ISO_CONSTRUCTION_TYPE',
                'num_stories':'NUM_STORIES',
                'original_year_built':'ORIGINAL_YEAR_BUILT',
                'BUILDING': 'POLICY_BUILDING',
                'BUSINESS PERSONAL PROPERTY':'POLICY_BPP',
                'BUSINESS INCOME WITH EXTRA EXPENSE':'POLICY_BI_EE',
                'OUTDOOR EXPENSE':'OUTDOOR_EXPENSE',
                'Total_TIV':'TOTAL_TIV',
                'occupancy_type':'OCCUPANCY_TYPE',
                'iso_protection_class':'ISO_PROTECTION_CLASS'}
            df_policy.rename(columns=col_dict, inplace=True)
            column_titles = ['FILENAME', 'POLICY_NO', 'POLICY_EFF_DATE', 'INSURED', 'POLICY_PREMNO', 'POLICY_BLDGNO', 'POLICY_STREET_ADDRESS', 'POLICY_CITY', 'POLICY_STATE', 'POLICY_ZIP', 'ISO_CONSTRUCTION_TYPE', 'NUM_STORIES', 'ORIGINAL_YEAR_BUILT', 'POLICY_BUILDING', 'POLICY_BPP', 'POLICY_BI_EE', 'OUTDOOR_EXPENSE', 'TOTAL_TIV', 'OCCUPANCY_TYPE', 'ISO_PROTECTION_CLASS']
            df_policy_final = df_policy.reindex(columns=column_titles)
            df_policy_final.fillna("NULL", inplace= True)
            df_policy_final =df_policy_final.astype(str)
            df_policy_final.to_gbq(
            destination_table=TABLE,
            project_id=PROJECT_ID,
            chunksize=10000,
            if_exists='append')
            polnolist =df_policy_final['POLICY_NO'].unique().tolist()
            polnos =''.join(polnolist)
            storage_client = storage.Client()
            storage_client.get_bucket(BUCKET_NAME).blob(
                        "Policy/Import/" +
                        polnos +
                        '.csv').upload_from_string(
                        df_policy_final.to_csv(),
                        'text/csv')
            return df_policy_final, 'success', 200
        except Exception as _:
            print("Exception", _)
            print("I am here", filename)
            policyno, eff_date, insured = policyno_eff_date_insured(texts)
            df_policy = coverage_table_2_creation(document, filename, doc_obj_list)
            #df_policy.drop_duplicates(keep='last', inplace = True)
            df_policy['filename'] = filename
            df_policy['policyno'] = policyno
            df_policy['eff_date'] = eff_date
            df_policy['insured'] = insured
            colums = ['street_address', 
                     'city', 
                     'state',
                     'zip',
                     'BUILDING', 
                     'BUSINESS PERSONAL PROPERTY', 
                     'BUSINESS INCOME WITH EXTRA EXPENSE', 
                     'OUTDOOR EXPENSE', 
                     'Total_TIV', 
                     'occupancy_type', 
                     'iso_protection_class']
            for cols in colums:
                df_policy[cols] = np.nan
            df_policy.replace(np.nan, "NULL", regex=True, inplace=True)
            
            print("1 df_policy_final", df_policy)
            df_policy.rename(
                columns={'filename': 'FILENAME', 'policyno': 'POLICY_NO', 'eff_date': 'POLICY_EFF_DATE', 'insured':'INSURED', 'premno':'POLICY_PREMNO', 'bldgno':'POLICY_BLDGNO', 'street_address':'POLICY_STREET_ADDRESS', 'city':'POLICY_CITY', 'state':'POLICY_STATE', 'zipcode':'POLICY_ZIP', 'construction':'ISO_CONSTRUCTION_TYPE', 'num_stories':'NUM_STORIES', 'original_year_built':'ORIGINAL_YEAR_BUILT', 'BUILDING': 'POLICY_BUILDING', 'BUSINESS PERSONAL PROPERTY':'POLICY_BPP', 'BUSINESS INCOME WITH EXTRA EXPENSE':'POLICY_BI_EE', 'OUTDOOR EXPENSE':'OUTDOOR_EXPENSE', 'Total_TIV':'TOTAL_TIV', 'occupancy_type':'OCCUPANCY_TYPE', 'iso_protection_class':'ISO_PROTECTION_CLASS'}, inplace=True)
            print("2 df_policy_final", df_policy)
            column_titles = ['FILENAME', 'POLICY_NO', 'POLICY_EFF_DATE', 'INSURED', 'POLICY_PREMNO', 'POLICY_BLDGNO', 'POLICY_STREET_ADDRESS', 'POLICY_CITY', 'POLICY_STATE', 'POLICY_ZIP', 'ISO_CONSTRUCTION_TYPE', 'NUM_STORIES', 'ORIGINAL_YEAR_BUILT', 'POLICY_BUILDING', 'POLICY_BPP', 'POLICY_BI_EE', 'OUTDOOR_EXPENSE', 'TOTAL_TIV', 'OCCUPANCY_TYPE', 'ISO_PROTECTION_CLASS']
            df_policy_final = df_policy.reindex(columns=column_titles)
            df_policy_final =df_policy_final.astype(str)
            df_policy_final.to_gbq(
            destination_table=TABLE,
            project_id=PROJECT_ID,
            chunksize=10000,
            if_exists='append'
            )
            polnolist =df_policy_final['POLICY_NO'].unique().tolist()
            polnos =''.join(polnolist)
            storage_client = storage.Client()
            storage_client.get_bucket(BUCKET_NAME).blob(
                        "Policy/Import/" +
                        polnos +
                        '.csv').upload_from_string(
                        df_policy_final.to_csv(),
                        'text/csv')
            return df_policy_final, 'success', 200
    except:
        #print(str(traceback.format_exc()),"********** Failed in Policy Document **********")
        return {"error": str(traceback.format_exc())}, 'failed', 500
