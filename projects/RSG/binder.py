import traceback
import json
import numpy as np
import pandas as pd
import json
import proto
import re
from google.cloud import storage

with open('config_ee.json') as f:
    config = json.load(f)

PROJECT_ID= config['project_id']
TABLE = config['table_binder_rsg']
BUCKET_NAME = 'rsg-data-tagging'

def dates_policyno(texts, filename):
    """Extract the policy number,Effective Date,Expiry Date"""
    dfpol_date = pd.DataFrame()
    polind = eval(
        "".join([str(i) for i, elem in enumerate(texts) if "Policy #:" in elem])
    )
    policynum = texts[polind].split(":")[1].strip()
    effdateind = eval(
        [str(i) for i, elem in enumerate(texts) if "Eff Date:" in elem][0]
    )
    effective_date = texts[effdateind].split(":")[1].strip()
    expdateind = eval(
        [str(i) for i, elem in enumerate(texts) if "Exp Date:" in elem][0]
    )
    expiry_date = texts[expdateind].split(":")[1].strip()
    dfpol_date["Document_name"] = [filename]
    dfpol_date["Policy_number"] = [policynum]
    dfpol_date["Effective_Date"] = [effective_date]
    dfpol_date["Expiry_Date"] = [expiry_date]

    return dfpol_date


def _get_text(el, document):
    """Convert text offset indexes into text snippets."""
    response = ""
    for segment in el.text_anchor.text_segments:
        start_index = segment.start_index
        end_index = segment.end_index
        response += document.text[start_index:end_index]
    return response


def processbinderdocument(document, filename, doclist,aopcount=1):
    """Processing the Document using the Table Extraction API to extract relevant tables"""
    txtstr = " ".join(document.text.split("\n"))
    texts = document.text.split("\n")
    if "Pol#:" in txtstr:
        poldf = dates_policyno(texts, filename)
    for doc in doclist:
        
        for page in doc.pages:
           
            for _, table in enumerate(page.tables):
                for row_num, row in enumerate(table.header_rows):
                    cells = "".join(
                        [_get_text(cell.layout, doc) for cell in row.cells]
                    )
                    if 'WIND' in cells:
                        for row_num, row in enumerate(table.body_rows):
                            cells = ([_get_text(cell.layout,doc) for cell in row.cells])
                            if cells[0]!='Coverage\n':
                                tmp =[aopcount]
                                cells.extend(tmp)
                                aopded.append(cells)
                        aopcount =aopcount+1
                    if cells[0].isdigit() and cells[1] == "/":
                        for row_num, row in enumerate(table.body_rows):
                            cells = [_get_text(cell.layout, doc) for cell in row.cells]
                            if cells[6][1].isdigit():
                                tmp = [aopcount]
                                cells.extend(tmp)
                                cells.pop(1)
                                aopded.append(cells)

                        aopcount = aopcount + 1

                    if cells[0].isdigit() and cells[1].isdigit() and cells[2].isdigit():
                        for row_num, row in enumerate(table.body_rows):
                            cells = [_get_text(cell.layout, doc) for cell in row.cells]
                            iso_code.append(cells)
                    if cells[0].isdigit():
                        for row_num, row in enumerate(table.body_rows):
                            cells = [_get_text(cell.layout, doc) for cell in row.cells]
                            try:

                                if cells[3][0].isdigit() and cells[3][1].isdigit():
                                    iso_code.append(cells)
                            except Exception as e:
                                pass

                    if (
                        "Bldg #" in cells
                        and "Year Built" in cells
                        and "Construction" in cells
                    ):

                        for row_num, row in enumerate(table.body_rows):

                            cells = [_get_text(cell.layout, doc) for cell in row.cells]

                            if len(cells) > 7:

                                cells[1] = cells[1] + cells[2] + cells[3]
                                res2 = "".join(
                                    [i for i in cells[4].split() if not i.isdigit()]
                                )
                                cells[2] = res2
                                res = "".join([i for i in cells[4].split() if i.isdigit()])
                                cells[3] = res
                                cells.pop(4)
                                iso_code.append(cells)
                            elif "WIND" in cells[-2]:
                                iso_code.append(cells)
                            else:
                                iso_code.append(cells)

                    if "AOP Ded" in cells and "Limit" in cells and "Coinsurance" in cells:

                        for row_num, row in enumerate(table.body_rows):
                            cells = [_get_text(cell.layout, doc) for cell in row.cells]
                            templ = []
                            if len(cells) < 8:
                                templ = [""]
                                templ.extend(cells)
                                tmp = [aopcount]
                                templ.extend(tmp)
                                aopded.append(templ)

                            else:
                                tmp = [aopcount]
                                cells.extend(tmp)
                                aopded.append(cells)

                        aopcount = aopcount + 1
    
    return iso_code, aopded, poldf


def iso_code_data(iso_code, aopded):
    """Extracting the location details from table"""
    iso_code2 = []
    for ghf in iso_code:
        if len(ghf) >= 4:
            iso_code2.append(ghf)

    iso_code = iso_code2.copy()
    iso_code2=[]
    jg =[sum(1 for x in w if x == '') for w in iso_code]
    
    for k in range(len(jg)):
        if jg[k]<4:
            iso_code2.append(iso_code[k])
    iso_code =iso_code2.copy()
    
    for ty in iso_code:
        if ty[0]=='':
            ty[0]='NULL' 
    iso_code2=[]
    for i in iso_code:
        if len(i)==9:
            if i[0][0].isdigit():
                i[1]=i[1]+i[2]+i[3]
                tmp=[]
                tmp.append(i[0])
                tmp.append(i[1])
                tmp.append(i[4])
                tmp.append(i[5])
                tmp.append(i[6])
                tmp.append(i[7])
                tmp.append(i[8])
                iso_code2.append(tmp)
        else:
            iso_code2.append(i)
    iso_code =iso_code2.copy()
    for gth in iso_code:
        gds =gth[2].replace('\n','')
        resd="".join(re.findall(r'\d+', gth[2]))
        if len(gth)==6:
            if len(resd)==2 and len(gth[0])==4:
                rd=gth[5]
                md=gth[4]
                pds=gth[3]
                gth.extend([rd])
                gth[5]=md
                gth[4]=pds
                gth[3]=resd
                mj =gds.replace(resd,'')
                gth[2]=mj
            if len(resd)==2 and len(gth[0])>5:
                rd=gth[5]
                md=gth[4]
                pds=gth[3]
                fd =gth[2]
                sd =gth[1]
                gth.extend([rd])
                gth[5]=md
                gth[4]=pds
                gth[3]=fd
                gth[2]=sd
                fz=gth.partition('\n')
                gth[0]=fz[0]
                gth[1]=fz[2]

    for iss in iso_code:
        dks =iss[3].replace('\n','')
        if len(iss)==6:
            if len(iss[3])==8 and dks.isdigit():

                rd =iss[5]
                sd=iss[4]
                iss.extend([rd])
                iss[5] =sd
                fck ="".join(re.findall(r'[1,2][9,0]\d{2}', dks))
                iss[4] =fck
                iss[3]=dks.replace(fck,'')
            
    iso_code3=[]
    for ij in iso_code:
        if (ij[0]=='') and (ij[1]=='') and (ij[2]==''):
            iso_code3.append(ij)
    for ik in iso_code3:
        iso_code.remove(ik)

    for isd in iso_code:
        ssd = " ".join(isd)
        gdf = isd[1].replace("\n", "")
        dsf = gdf.rpartition("NON-COMBUST IBLE")
        sdf = isd[3].replace("\n", "")
        edf = sdf.replace(" ", "")
        if (
            isd[0][0].isdigit()
            and "NON-COMBUST" in ssd
            and len(isd) == 7
            and isd[2] == ""
            and "-" in edf
        ):
            res1 = "".join(re.findall("[a-zA-Z\-]+", isd[3]))
            res2 = "".join(re.findall(r"\d+", isd[3]))
            isd[2] = res1
            isd[3] = res2
        if (
            isd[0][0].isdigit()
            and "NON-COMBUST" in ssd
            and len(isd) == 7
            and isd[2] == ""
            and edf.isdigit()
        ):
            isd[2] = dsf[1]
            isd[1] = dsf[0]
        if (
            isd[0][0].isdigit()
            and "NON-COMBUST" in ssd
            and len(isd) == 7
            and isd[2] != ""
            and "-" in edf
        ):
            isd[1] = isd[1] + isd[2]
            rs1 = "".join(re.findall("[a-zA-Z\-]+", isd[3]))
            rs2 = "".join(re.findall(r"\d+", isd[3]))
            isd[2] = rs1
            isd[3] = rs2
        if (
            isd[0][0].isdigit()
            and "FRAME" in ssd
            and len(isd) == 7
            and isd[2] != ""
            and edf == "FRAME02"
        ):
            isd[1] = isd[1] + isd[2]
            rs1 = "".join(re.findall("[a-zA-Z\-]+", isd[3]))
            rs2 = "".join(re.findall(r"\d+", isd[3]))
            isd[2] = rs1
            isd[3] = rs2

    for isd in iso_code:
        ssd = " ".join(isd)
        sdf = isd[3].replace("\n", "")
        edf = sdf.replace(" ", "")
        if (
            isd[0][0].isdigit()
            and "NON-COMBUST" in ssd
            and len(isd) == 7
            and isd[2] == ""
            and (edf.isalnum() or "-" in edf)
        ):
            res1 = "".join(re.findall("[a-zA-Z\-]+", isd[3]))
            res2 = "".join(re.findall(r"\d+", isd[3]))
            isd[2] = res1
            isd[3] = res2

    for iso in iso_code:
        ssd = " ".join(iso)
        if iso[0][0].isdigit() and "MASO" in ssd and len(iso) == 8:
            iso[1] = iso[1] + iso[2]
            iso.pop(2)

    cld = 1
    for i in iso_code:
        if i[0] == "BUILDING\n" and i[2].isalpha():
            tj = [cld]
            i.extend(tj)
            aopded.append(i)
            cld = cld + 1


    if iso_code[0][0] == "" and iso_code[0][1] == "" and iso_code[0][2] == "":
        iso_code.pop(0)

    iso_code_final = []
    for i in iso_code:
        if len(i[0]) < 7 and len(i) == 7 and i[5][3].isalpha():
            iso_code_final.append(i)

    iso_code_df = []
    count = 1
    for h in iso_code_final:
        valappend = count
        lgh = [valappend]
        h.extend(lgh)
        iso_code_df.append(h)
        count = count + 1
    iso_code_df2=[]
    for gs in iso_code_df:
        if gs[0]!='the ':
            iso_code_df2.append(gs)
    iso_code_df =iso_code_df2.copy()
    iso_code_df2=[]
    for gs in iso_code_df:
        if gs[0][0].isdigit():
            iso_code_df2.append(gs)
    iso_code_df =iso_code_df2.copy()    
    
    dfiso = pd.DataFrame(
        iso_code_df,
        columns=[
            "loc/Bldg",
            "ISO_code_description",
            "Construction",
            "PC",
            "Year_Built",
            "Wind/Hail",
            "Wind/Hail_ded",
            "common_key",
        ],
    )
    dfiso["common_key"] = np.where(
        dfiso["common_key"].isnull(), dfiso["Wind/Hail_ded"], dfiso["common_key"]
    )
    
    return dfiso, aopded


def cov_data(aopded):
    """Extracting the coverage details table"""
    aopded_final2=[]
    jg =[sum(1 for x in w if x == '') for w in aopded]
    for k in range(len(jg)):
        if jg[k]<5:
            aopded_final2.append(aopded[k])
    aopded =aopded_final2.copy() 
    
    aopded_final = []
    for j in aopded:
        if j[5] != "" and len(j) == 9:
            aopded_final.append(j)

    aopded_final2 = []
    for k in aopded_final:
        gds = k[5]
        if "Property Premium" not in gds:
            aopded_final2.append(k)
    
    dfaop = pd.DataFrame(
        aopded_final2,
        columns=[
            "Coverage",
            "Cause of Loss",
            "Valuation",
            "Coinsurance",
            "AOP Ded",
            "Limit",
            "Rate",
            "Premium",
            "common_key",
        ],
    )

    onlybl = dfaop["Coverage"].unique().tolist()
    if len(onlybl) == 2:
        if "" in onlybl:
            dfaop.loc[dfaop["Coverage"] == "", ["Coverage"]] = onlybl[0]
    return dfaop


def cov_iso_data(dfiso, dfaop, filename):
    """Combining the coverage details table & the location table based on tables"""
    finaldf = pd.merge(dfiso, dfaop, how="outer", on="common_key")
    finaldf.drop("common_key", axis=1, inplace=True)
    fl = filename
    documentname = []
    for s in range(finaldf.shape[0]):
        documentname.append(fl)
    finaldf["Document_name"] = documentname
    
    return finaldf

def binderesprocess(document,filename):

    for page in document.pages:
        for table_num, table in enumerate(page.tables):
            for row_num, row in enumerate(table.header_rows):
                cells = "".join([_get_text(cell.layout,document) for cell in row.cells])
                

                if 'SUBJECTS OF INSURANCE' in cells and 'Value' in cells and 'Coinsurance' in cells and 'Valuation' in cells:
                    for row_num, row in enumerate(table.body_rows):
                        cells = ([_get_text(cell.layout,document) for cell in row.cells])
                        bxcov.append(cells)
    return bxcov

def bxcovdata(document,bxcov,filename): 
    dfbxcov =pd.DataFrame(bxcov,columns=['Coverage','Limit','Coinsurance','Valuation'])
    dfbxcov =dfbxcov.iloc[:-1:]
    dfbxcov.drop(['Coinsurance','Valuation'],axis=1,inplace=True)
    dfbxcov = pd.get_dummies(dfbxcov, columns = ['Coverage'], prefix='', prefix_sep='')
    dfbxcov.rename(columns={'Business Income w/ Extra Expense - Per Statement of Values\n':'BINDER_BI_EE','Buildings Per Statement of Values\n':'BINDER_BUILDING','Business Personal Property - Per Statement of Values\n':'BINDER_BPP'},inplace=True)
    covcols=['BINDER_BUILDING','BINDER_BI_EE','BINDER_BPP']
    for i in covcols:
        dfbxcov[i] = np.where(dfbxcov[i]==1, dfbxcov['Limit'], np.nan)
    txtstr = " ".join(document.text.split("\n"))
    Getpol =txtstr.split('Assigned Policy Number: ')
    polno=Getpol[1].split(' ')[0]
    GetEff =txtstr.split('Effective Dates: ')
    Getdates =GetEff[1].split('to')
    Effdate=Getdates[0].strip()
    Expdate =Getdates[1].split(' ')[1]
    dfbxcov['BINDER_EFFECTIVE_DATE']=Effdate
    dfbxcov['BINDER_EXPIRY_DATE']=Expdate
    dfbxcov['BINDER_POLICY_NUMBER']=polno
    dfbxcov.drop(['Limit'],axis=1,inplace=True)
    dfbxcov = dfbxcov.fillna(np.nan).groupby(['BINDER_EFFECTIVE_DATE', 'BINDER_EXPIRY_DATE'], as_index=False).first()
    return dfbxcov

def binder_main(document, filename,doclist):
    """Main function of Binder which will be returning the dataframe after processing the coverage table & location table"""
    
    global iso_code
    global aopded
    global bxcov
    iso_code = []
    aopded = []
    bxcov=[]
    try:
        try:
            aopcount = 1
            iso_code, aopded, poldf = processbinderdocument(document, filename, doclist,aopcount=1)
            dfiso, aopded = iso_code_data(iso_code, aopded)
            dfaop = cov_data(aopded)
            finaldf = cov_iso_data(dfiso, dfaop, filename)
            final = finaldf.merge(poldf, how="inner", on="Document_name")
            
            dfcovtmp = final[["Coverage", "loc/Bldg"]]
            final.drop(["Coverage", "loc/Bldg"], axis=1, inplace=True)
            dfcovtmp.replace("\n", "", regex=True, inplace=True)
            final.replace("\n", " ", regex=True, inplace=True)
            final2 = pd.concat([final, dfcovtmp], axis=1)
            final2.fillna("NULL", inplace=True)
            loc_bldg = final2["loc/Bldg"].tolist()
            loc_bldg2=[]
            for j in loc_bldg:
                if j=='311':
                    ss=j.replace('311','3/1')
                    loc_bldg2.append(ss)
                elif j=='111':
                    ss=j.replace('111','1/1')
                    loc_bldg2.append(ss)
                elif j=='211':
                    ss=j.replace('211','2/1')
                    loc_bldg2.append(ss)
                elif j=='411':
                    ss=j.replace('411','4/1')
                    loc_bldg2.append(ss)
                elif j=='511':
                    ss=j.replace('511','5/1')
                    loc_bldg2.append(ss)
                elif j=='611':
                    ss=j.replace('611','6/1')
                    loc_bldg2.append(ss)
                elif j=='711':
                    ss=j.replace('711','7/1')
                    loc_bldg2.append(ss)
                elif j=='811':
                    ss=j.replace('811','8/1')
                    loc_bldg2.append(ss)
                elif j=='911':
                    ss=j.replace('911','9/1')
                    loc_bldg2.append(ss)
                else:
                    loc_bldg2.append(j)
            loc_bldg=loc_bldg2.copy()
            
            Loc = []
            Bldg = []
            for locbl in loc_bldg:
                if locbl != "NULL":

                    if "/" in locbl:
                        Loc.append(locbl.split("/")[0])
                        Bldg.append(locbl.split("/")[1])
                    else:
                        if locbl[0] != 7:
                            Loc.append(locbl.split("7")[0])
                            Bldg.append(locbl.split("7")[1])
                else:
                    Loc.append("NULL")
                    Bldg.append("NULL")

            final2["Loc#"] = Loc
            final2["Bldg#"] = Bldg
            
            final2.drop(["loc/Bldg"], axis=1, inplace=True)
            
            final2.drop(
                [
                    "ISO_code_description",
                    "Cause of Loss",
                    "Valuation",
                    "Coinsurance",
                    "Rate",
                    "Premium",
                ],
                axis=1,
                inplace=True,
            )
            
            uniqcov = final2["Coverage"].unique().tolist()
            finaldf2 = pd.get_dummies(
                final2, columns=["Coverage"], prefix="", prefix_sep=""
            )
            covuncols = ["BUILDING", "BPP", "BI/EE", "PIO", "TI&B"]
            covcolsrem = list(set(covuncols) - set(uniqcov))
            for kh in covcolsrem:
                finaldf2[kh] = np.nan
            for i in covuncols:
                finaldf2[i] = np.where(finaldf2[i] == 1, finaldf2["Limit"], np.nan)
            finaldf2["AOP Ded_BI/EE"] = np.nan
            finaldf2["AOP Ded_BPP"] = np.nan
            finaldf2["AOP Ded_BUILDING"] = np.nan
            finaldf2["AOP Ded_TI&B"] = np.nan
            finaldf2["AOP Ded_PIO"] = np.nan
            aopcols = [
                "AOP Ded_BI/EE",
                "AOP Ded_BPP",
                "AOP Ded_BUILDING",
                "AOP Ded_TI&B",
                "AOP Ded_PIO",
            ]
            for i in aopcols:
                finaldf2[i] = np.where(
                    finaldf2[i.split("_")[-1]].notnull(), finaldf2["AOP Ded"], np.nan
                )
            finaldf2.drop(["AOP Ded", "Limit"], axis=1, inplace=True)
            finaldf2 = finaldf2.reindex(sorted(finaldf2.columns), axis=1)
            finaldf2.replace(np.nan, "NULL", regex=True, inplace=True)
            finaldf2.replace("", "NULL", regex=True, inplace=True)
            finaldf2.replace("NULL", np.nan, regex=True, inplace=True)
            if finaldf2.shape[0] == 1:
                finaldf2.replace(np.nan, "NULL", regex=True, inplace=True)
                dffinal3 = finaldf2.reindex(sorted(finaldf2.columns), axis=1)
                dffinal3.rename(
                    columns={
                        "AOP Ded_BI/EE": "AOP_DED_BI_EE",
                        "AOP Ded_BPP": "AOP_DED_BPP",
                        "AOP Ded_BUILDING": "AOP_DED_BUILDING",
                        "AOP Ded_PIO": "AOP_DED_PIO",
                        "AOP Ded_TI&B": "AOP_DED_TI_B",
                        "Wind/Hail": "WIND_HAIL",
                        "Wind/Hail_ded": "WIND_HAIL_DED",
                        "TI&B": "BINDER_TI_B",
                        "BI/EE": "BINDER_BI_EE",
                        "Bldg#": "BINDER_BLDG",
                        "Loc#": "BINDER_PREM_NO",
                        "BPP":"BINDER_BPP",
                        "BUILDING":"BINDER_BUILDING",
                        "Construction":"BINDER_ISO_CONSTRUCTION_TYPE",
                        "PC":"BINDER_ISO_PROTECTION_CLASS",
                        "PIO":"BINDER_PIO",
                        "Year_Built":"BINDER_ORIGINAL_YEAR_BUILT",
                        "Document_name":"DOCUMENT_NAME",
                        "Policy_number":"BINDER_POLICY_NUMBER",
                        "Effective_Date":"BINDER_EFFECTIVE_DATE",
                        "Expiry_Date":"BINDER_EXPIRY_DATE"
                    },
                    inplace=True,
                )
                
                dffinal3 = dffinal3.astype(str)
                
                dffinal3 = dffinal3.drop(['','NULL'], axis=1, errors='ignore')
                #if 'NULL' in dffinal3.columns.tolist():
                    #dffinal3.drop(['NULL'],axis=1,inplace=True)
                dffinal3.drop_duplicates(keep='first',inplace=True)
                #dffinal3.to_csv(r'result0.csv',index=False)
                polnolist =dffinal3['BINDER_POLICY_NUMBER'].unique().tolist()
                polnos =''.join(polnolist)
                if len(dffinal3)==0:
                    dffinal3['DOCUMENT_NAME']=poldf['Document_name']
                    dffinal3['BINDER_EFFECTIVE_DATE']=poldf['Effective_Date']
                    dffinal3['BINDER_EXPIRY_DATE']=poldf['Expiry_Date']
                    dffinal3['BINDER_POLICY_NUMBER']=poldf['Policy_number']
                dffinal3.replace(np.nan,'NULL',regex=True,inplace=True)
                dffinal3.replace('','NULL',regex=True,inplace=True)
                dffinal3['DOCUMENT_NAME'] = np.where(dffinal3['DOCUMENT_NAME'] == 'NULL', dffinal3["BINDER_ORIGINAL_YEAR_BUILT"], dffinal3['DOCUMENT_NAME'])
                storage_client = storage.Client()
                storage_client.get_bucket(BUCKET_NAME).blob(
                        "Binders/Import/" +
                        polnos +
                        '.csv').upload_from_string(
                        dffinal3.to_csv(),
                        'text/csv')              
                
                dffinal3.to_gbq(
                    destination_table=TABLE,
                    project_id=PROJECT_ID,
                    chunksize=10000,
                    if_exists="append",
                )
                #dffinal3.to_csv(r'result1.csv',index=False)
                return dffinal3,'success',200

            if finaldf2.shape[0] != 1:
                dffinal3 = (
                    finaldf2.fillna(np.nan)
                    .groupby(
                        [
                            "Loc#",
                            "Bldg#",
                            "Policy_number",
                            "Effective_Date",
                            "Expiry_Date",
                            # "Construction",
                            # "PC",
                            # "Year_Built",
                        ],
                        as_index=False,
                    )
                    .first()
                )
                dffinal3.replace(np.nan, "NULL", regex=True, inplace=True)
                dffinal3 = dffinal3.reindex(sorted(dffinal3.columns), axis=1)
                dffinal3.rename(
                    columns={
                        "AOP Ded_BI/EE": "AOP_DED_BI_EE",
                        "AOP Ded_BPP": "AOP_DED_BPP",
                        "AOP Ded_BUILDING": "AOP_DED_BUILDING",
                        "AOP Ded_PIO": "AOP_DED_PIO",
                        "AOP Ded_TI&B": "AOP_DED_TI_B",
                        "Wind/Hail": "WIND_HAIL",
                        "Wind/Hail_ded": "WIND_HAIL_DED",
                        "TI&B": "BINDER_TI_B",
                        "BI/EE": "BINDER_BI_EE",
                        "Bldg#": "BINDER_BLDG",
                        "Loc#": "BINDER_PREM_NO",
                        "BPP":"BINDER_BPP",
                        "BUILDING":"BINDER_BUILDING",
                        "Construction":"BINDER_ISO_CONSTRUCTION_TYPE",
                        "PC":"BINDER_ISO_PROTECTION_CLASS",
                        "PIO":"BINDER_PIO",
                        "Year_Built":"BINDER_ORIGINAL_YEAR_BUILT",
                        "Document_name":"DOCUMENT_NAME",
                        "Policy_number":"BINDER_POLICY_NUMBER",
                        "Effective_Date":"BINDER_EFFECTIVE_DATE",
                        "Expiry_Date":"BINDER_EXPIRY_DATE"
                    },
                    inplace=True,
                )
                
                dffinal3 = dffinal3.astype(str)
                
                
                dffinal3 = dffinal3.drop(['','NULL'], axis=1, errors='ignore')
                #if 'NULL' in dffinal3.columns.tolist():
                    #dffinal3.drop(['NULL'],axis=1,inplace=True)
                dffinal3.drop_duplicates(keep='first',inplace=True)
                #dffinal3.to_csv(r'result0.csv',index=False)
                polnolist =dffinal3['BINDER_POLICY_NUMBER'].unique().tolist()
                polnos =''.join(polnolist)
                if len(dffinal3)==0:
                    dffinal3['DOCUMENT_NAME']=poldf['Document_name']
                    dffinal3['BINDER_EFFECTIVE_DATE']=poldf['Effective_Date']
                    dffinal3['BINDER_EXPIRY_DATE']=poldf['Expiry_Date']
                    dffinal3['BINDER_POLICY_NUMBER']=poldf['Policy_number']
                dffinal3.replace(np.nan,'NULL',regex=True,inplace=True)
                dffinal3.replace('','NULL',regex=True,inplace=True)
                dffinal3['DOCUMENT_NAME'] = np.where(dffinal3['DOCUMENT_NAME'] == 'NULL', dffinal3["BINDER_ORIGINAL_YEAR_BUILT"], dffinal3['DOCUMENT_NAME'])
                storage_client = storage.Client()
                storage_client.get_bucket(BUCKET_NAME).blob(
                        "Binders/Import/" +
                        polnos +
                        '.csv').upload_from_string(
                        dffinal3.to_csv(),
                        'text/csv')   
                
                dffinal3.to_gbq(
                    destination_table=TABLE,
                    project_id=PROJECT_ID,
                    chunksize=10000,
                    if_exists="append",
                )
                #dffinal3.to_csv(r'result1.csv',index=False)
                return dffinal3,'success',200

        except Exception as e:
            
            txtstr = " ".join(document.text.split("\n"))
            texts = document.text.split("\n")
            if "Pol#:" in txtstr:
                colsd = [
                    "AOP Ded_BI/EE",
                    "AOP Ded_BPP",
                    "AOP Ded_BUILDING",
                    "AOP Ded_PIO",
                    "AOP Ded_TI&B",
                    "BI/EE",
                    "BPP",
                    "BUILDING",
                    "Bldg#",
                    "Construction",
                    "Loc#",
                    "PC",
                    "PIO",
                    "TI&B",
                    "Wind/Hail",
                    "Wind/Hail_ded",
                    "Year_Built",
                ]
                dfg = pd.DataFrame()
                poldf = dates_policyno(texts, filename)

                for h in colsd:
                    dfg[h] = np.nan

                dfg.fillna("NULL", inplace=True)
                finalh = pd.concat([dfg, poldf], axis=1, ignore_index=True)
                finalh.columns = [
                    "AOP Ded_BI/EE",
                    "AOP Ded_BPP",
                    "AOP Ded_BUILDING",
                    "AOP Ded_PIO",
                    "AOP Ded_TI&B",
                    "BI/EE",
                    "BPP",
                    "BUILDING",
                    "Bldg#",
                    "Construction",
                    "Document_name",
                    "Loc#",
                    "PC",
                    "PIO",
                    "TI&B",
                    "Wind/Hail",
                    "Wind/Hail_ded",
                    "Year_Built",
                    "Policy_number",
                    "Effective_Date",
                    "Expiry_Date",
                ]

                finalh2 = finalh.reindex(sorted(finalh.columns), axis=1)

                finalh2.rename(
                    columns={
                        "AOP Ded_BI/EE": "AOP_DED_BI_EE",
                        "AOP Ded_BPP": "AOP_DED_BPP",
                        "AOP Ded_BUILDING": "AOP_DED_BUILDING",
                        "AOP Ded_PIO": "AOP_DED_PIO",
                        "AOP Ded_TI&B": "AOP_DED_TI_B",
                        "Wind/Hail": "WIND_HAIL",
                        "Wind/Hail_ded": "WIND_HAIL_DED",
                        "TI&B": "BINDER_TI_B",
                        "BI/EE": "BINDER_BI_EE",
                        "Bldg#": "BINDER_BLDG",
                        "Loc#": "BINDER_PREM_NO",
                        "BPP":"BINDER_BPP",
                        "BUILDING":"BINDER_BUILDING",
                        "Construction":"BINDER_ISO_CONSTRUCTION_TYPE",
                        "PC":"BINDER_ISO_PROTECTION_CLASS",
                        "PIO":"BINDER_PIO",
                        "Year_Built":"BINDER_ORIGINAL_YEAR_BUILT",
                        "Document_name":"DOCUMENT_NAME",
                        "Policy_number":"BINDER_POLICY_NUMBER",
                        "Effective_Date":"BINDER_EFFECTIVE_DATE",
                        "Expiry_Date":"BINDER_EXPIRY_DATE"
                    },
                    inplace=True,
                )
                
                finalh2 = finalh2.astype(str)
                finalh2 = finalh2.drop(['','NULL'], axis=1, errors='ignore')
                finalh2.replace(np.nan, "NULL", regex=True, inplace=True)
                finalh2.fillna("NULL",inplace=True)
                finalh2.replace('nan','NULL',regex=True,inplace=True)
                finalh2.drop_duplicates(keep='first',inplace=True)
                #finalh2.to_csv(r'result0.csv',index=False)
                polnolist =finalh2['BINDER_POLICY_NUMBER'].unique().tolist()
                polnos =''.join(polnolist)
                if len(finalh2)==0:
                    finalh2['DOCUMENT_NAME']=poldf['Document_name']
                    finalh2['BINDER_EFFECTIVE_DATE']=poldf['Effective_Date']
                    finalh2['BINDER_EXPIRY_DATE']=poldf['Expiry_Date']
                    finalh2['BINDER_POLICY_NUMBER']=poldf['Policy_number']
                finalh2.replace(np.nan,'NULL',regex=True,inplace=True)
                finalh2.replace('','NULL',regex=True,inplace=True)
                finalh2['DOCUMENT_NAME'] = np.where(finalh2['DOCUMENT_NAME'] == 'NULL', finalh2["BINDER_ORIGINAL_YEAR_BUILT"], finalh2['DOCUMENT_NAME'])
                storage_client = storage.Client()
                storage_client.get_bucket(BUCKET_NAME).blob(
                        "Binders/Import/" +
                        polnos +
                        '.csv').upload_from_string(
                        finalh2.to_csv(),
                        'text/csv')
                finalh2.to_gbq(
                    destination_table=TABLE,
                    project_id=PROJECT_ID,
                    chunksize=10000,
                    if_exists="append",
                )
                #finalh2.to_csv(r'result1.csv',index=False)
                return finalh2,'success',200

            else:
                
                colsss = [
                    "AOP Ded_BI/EE",
                    "AOP Ded_BPP",
                    "AOP Ded_BUILDING",
                    "AOP Ded_PIO",
                    "AOP Ded_TI&B",
                    "BI/EE",
                    "BINDER_BPP",
                    "BINDER_BUILDING",
                    "Bldg#",
                    "BINDER_ISO_CONSTRUCTION_TYPE",
                    "DOCUMENT_NAME",
                    "BINDER_EFFECTIVE_DATE",
                    "BINDER_EXPIRY_DATE",
                    "Loc#",
                    "BINDER_ISO_PROTECTION_CLASS",
                    "BINDER_PIO",
                    "BINDER_POLICY_NUMBER",
                    "TI&B",
                    "Wind/Hail",
                    "Wind/Hail_ded",
                    "BINDER_ORIGINAL_YEAR_BUILT",
                ]
                tmpdf = pd.DataFrame()
                for gdf in colsss:
                    tmpdf[gdf] = np.nan
                tmpdf.replace(np.nan, "NULL", regex=True, inplace=True)
                
                #tmpdf = tmpdf.reindex(sorted(tmpdf.columns), axis=1)
                tmpdf.rename(
                    columns={
                        "AOP Ded_BI/EE": "AOP_DED_BI_EE",
                        "AOP Ded_BPP": "AOP_DED_BPP",
                        "AOP Ded_BUILDING": "AOP_DED_BUILDING",
                        "AOP Ded_PIO": "AOP_DED_PIO",
                        "AOP Ded_TI&B": "AOP_DED_TI_B",
                        "Wind/Hail": "WIND_HAIL",
                        "Wind/Hail_ded": "WIND_HAIL_DED",
                        "TI&B": "BINDER_TI_B",
                        "BI/EE": "BINDER_BI_EE",
                        "Bldg#": "BINDER_BLDG",
                        "Loc#": "BINDER_PREM_NO",
                    },
                    inplace=True,
                )
                bxcov =binderesprocess(document,filename)
                tmpdf['DOCUMENT_NAME']=filename
                dfbxcov=bxcovdata(document,bxcov,filename)
                for colms in dfbxcov.columns:
                    tmpdf[colms]=dfbxcov[colms]
                tmpdf.replace(np.nan, "NULL", regex=True, inplace=True)   
                
                tmpdf = tmpdf.astype(str)
                tmpdf = tmpdf.drop(['','NULL'], axis=1, errors='ignore')
                tmpdf.drop_duplicates(keep='first',inplace=True)
                #tmpdf.to_csv(r'result0.csv',index=False)
                polnolist =tmpdf['BINDER_POLICY_NUMBER'].unique().tolist()
                polnos =''.join(polnolist)
                if len(tmpdf)==0:
                    tmpdf['DOCUMENT_NAME']=poldf['Document_name']
                    tmpdf['BINDER_EFFECTIVE_DATE']=poldf['Effective_Date']
                    tmpdf['BINDER_EXPIRY_DATE']=poldf['Expiry_Date']
                    tmpdf['BINDER_POLICY_NUMBER']=poldf['Policy_number']
                tmpdf.replace(np.nan,'NULL',regex=True,inplace=True)
                tmpdf.replace('','NULL',regex=True,inplace=True)
                tmpdf['DOCUMENT_NAME'] = np.where(tmpdf['DOCUMENT_NAME'] == 'NULL', tmpdf["BINDER_ORIGINAL_YEAR_BUILT"], tmpdf['DOCUMENT_NAME'])
                storage_client = storage.Client()
                storage_client.get_bucket(BUCKET_NAME).blob(
                        "Binders/Import/" +
                        polnos +
                        '.csv').upload_from_string(
                        tmpdf.to_csv(),
                        'text/csv')            
                tmpdf.to_gbq(
                    destination_table=TABLE,
                    project_id=PROJECT_ID,
                    chunksize=10000,
                    if_exists="append",
                )
                #tmpdf.to_csv('result1.csv',index=False)
                return tmpdf,'success',200

    except:
        print(str(traceback.format_exc()),"********** Failed in Binder Document **********")
        return {"error": str(traceback.format_exc())}, 'failed', 500 
