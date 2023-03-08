"""
This module takes form parser object for ACORD125 as input and gives the extracted results in the form of csv

Date created: 18/02/2022
Modified on: 21/02/2022
"""
# pylint: disable = W0703, R0913
import json
import re
import proto
import pandas as pd
from google.cloud import storage
from acord_helper import _get_text, get_y_coordinates, get_x_coordinates

with open('config_ee.json') as f:
    config = json.load(f)
    
#PROJECT_ID = "q-gcp-6508-rsg-docai-22-01"
#TABLE = "RSG.ACCORD125"
BUCKET_NAME = 'rsg-data-tagging'
PROJECT_ID= config['project_id']
TABLE = config['table_rsg']

def acord_125_page1(acord_data, page_no):
    """
    Function to extract entities : Proposed Exp Date and Proposed Eff Date
    """

    acord_dict = {}
    acord_dict["PROPOSED EFF DATE"] = "NULL"
    acord_dict["PROPOSED EXP DATE"] = "NULL"
    
    
    
    def get_bounds_forbilling(acord_data, page_no):
        """
        Function to get the Boundary coordinates for Expiry date
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            flag = -999
            for count, token in enumerate(
                    acord_data["pages"][page_no]["tokens"]):
                f_text = _get_text(acord_data, token, element_type="tokens")

                trial = re.sub(r"[\n\t\s]*", "", f_text)
                if trial == "BILLING":
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    y_min = y_2
                    x_max = x_2 + 10 * (x_2 - x_1)
                    x_bill = x_1
                    x_min = x_1 - 4 * (x_2 - x_1)
                    y_max = y_2 + 5 * (y_2 - y_1)
                    break
        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max, x_bill

    y_min, x_min, y_max, x_max, x_bill = get_bounds_forbilling(
        acord_data, page_no)
    
    def get_bounds_forproposedexpdate(acord_data, page_no):
        """
        Function to get the Boundary coordinates for Expiry date
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            flag = -999
            for count, token in enumerate(
                    acord_data["pages"][page_no]["tokens"]):
                f_text = _get_text(acord_data, token, element_type="tokens")

                trial = re.sub(r"[\n\t\s]*", "", f_text)
                if trial in ('EXP', 'EXPIRATION'):
                    flag = count
                if trial == "DATE":
                    if count < flag + 5:
                        x_1, x_2 = get_x_coordinates(token)
                        y_1, y_2 = get_y_coordinates(token)
                        y_min = y_2
                        x_max = x_2 + 10 * (x_2 - x_1)
                        x_exp = x_1
                        x_min = x_1 - 4 * (x_2 - x_1)
                        y_max = y_2 + 5 * (y_2 - y_1)
                        break
        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max, x_exp

    y_min, x_min, y_max, x_max, x_exp = get_bounds_forproposedexpdate(
        acord_data, page_no)

    def get_bounds_proposedexpdate(
            acord_data,
            page_no,
            y_min,
            x_min,
            y_max,
            x_bill):
        """
        Function to get the values for Expiry date
        """

        try:
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if (x_min < x_1 < x_2 < x_bill) and (y_min < y_1 < y_2 < y_max):
                    acord_dict["PROPOSED EXP DATE"] = trial
                    break
        except Exception as _:
            pass
        return trial

    _ = get_bounds_proposedexpdate(
        acord_data, page_no, y_min, x_min, y_max, x_bill
    )

    def get_bounds_forproposedeffdate(acord_data, page_no):
        """
        Function to get the Boundary for Effective Date
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            flag = -999
            for count, token in enumerate(
                    acord_data["pages"][page_no]["tokens"]):
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                if trial in ('EFF', 'EFFECTIVE'):
                    flag = count
                if trial == "DATE":
                    if count < flag + 5:
                        x_1, x_2 = get_x_coordinates(token)
                        y_1, y_2 = get_y_coordinates(token)                     
                                               
                        y_min = y_2
                        x_max = x_2 + 10 * (x_2 - x_1)
                        x_min = x_1 - 10 * (x_2 - x_1)
                        y_max = y_2 + 5 * (y_2 - y_1)
        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forproposedeffdate(
        acord_data, page_no)

    def get_bounds_proposedeffdate(
            acord_data,
            page_no,
            y_min,
            x_min,
            y_max,
            x_exp):
        """
        Function to get the values of Effective date
        """

        try:
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if (x_min < x_1 < x_2 < x_exp) and (y_min < y_1 < y_2 < y_max):
                    acord_dict["PROPOSED EFF DATE"] = trial
                    break
        except Exception as _:
            pass
        return trial

    _ = get_bounds_proposedeffdate(
        acord_data, page_no, y_min, x_min, y_max, x_exp
    )

    

    return acord_dict


def acord_125_page2(acord_data, page_no):
    """
    Function to extract entities: DESCRIPTION OF OPERATIONS,LOC #,BLD #,CITY,COUNTY,
    ZIP, STREET,STATE
    """

    acord_dict = {}
    acord_dict["DESCRIPTION OF OPERATIONS"] = []
    acord_dict["LOC #"] = []
    acord_dict["BLD #"] = []
    acord_dict["CITY"] = []
    acord_dict["COUNTY"] = []
    acord_dict["ZIP"] = []
    acord_dict["STREET"] = []
    acord_dict["STATE"] = []

    xmin_op, xmax_op, ymin_op, ymax_op = ([] for i in range(4))

    def get_list_descriptionofoperations(acord_data, page_no):
        """
        Function to get the Boundary for Description of Operations
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                if trial == "OPERATIONS":
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    xmin_op.append(x_1)
                    xmax_op.append(x_2)
                    ymin_op.append(y_1)
                    ymax_op.append(y_2)

        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max

    get_list_descriptionofoperations(acord_data, page_no)

    # for premises boundary
    def get_bounds_forpremises(acord_data, page_no):
        """
        Function to get the boundary for Premises
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                if trial == "PREMISES":
                    _, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    y_min = y_1
                    x_max = x_2
                    x_min = x_2
                    y_max = y_2
                    break

        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max

    _, _, yprem_max, _ = get_bounds_forpremises(
        acord_data, page_no
    )

    def get_bounds_fordescriptionofoperations(acord_data, page_no):
        """
        Function to get the Boundary for Description of Operations
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= yprem_max and y_2 <= 1.5 * ymin_op[0]:
                    if trial == "OPERATIONS":
                        y_min = y_1 - 20
                        x_max = x_2 + 8.5 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 20
                        break

        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_fordescriptionofoperations(
        acord_data, page_no
    )

    if y_min == 9999:
        acord_dict["DESCRIPTION OF OPERATIONS"].append("NULL")
    else:
        new_list = []

        def get_bounds_descriptionofoperations(
            acord_data, page_no, y_min, x_min, y_max, x_max
        ):
            """
            Function to get the values of Description of Operations
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):
                        new_list.append(trial)

            except Exception as _:
                pass
            return trial

        _ = get_bounds_descriptionofoperations(
            acord_data, page_no, y_min, x_min, y_max, x_max
        )
        if len(new_list) == 0:

            acord_dict["DESCRIPTION OF OPERATIONS"].append("NULL")
        else:
            acord125 = " ".join(new_list)

            acord_dict["DESCRIPTION OF OPERATIONS"].append(acord125)

    

    def get_bounds_forbld(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= yprem_max and y_2 <= 1.5 * ymin_op[0]:
                    if trial == "BLD":
                        y_min = y_2
                        x_max = x_2 + 20
                        x_min = x_1 - 5
                        y_max = y_2 + 3.5 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forbld(acord_data, page_no)

    if y_min == 9999:
        acord_dict["BLD #"].append("NULL")
    else:
        def get_bounds_bld(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):
                        acord_dict["BLD #"].append(trial)
                        break
            except Exception as _:
                pass
            return trial

        _ = get_bounds_bld(acord_data, page_no, y_min, x_min, y_max, x_max)

        if len(acord_dict["BLD #"]) == 0:
            acord_dict["BLD #"].append("NULL")
    
    
    def get_bounds_forloc(acord_data, page_no):
        """
        Function to get the Boundary For Loc
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= yprem_max and y_2 <= 1.5 * ymin_op[0]:
                    if trial == "LOC":
                        y_min = y_2
                        x_max = x_2 + 20
                        x_min = x_1 - 5
                        y_max = y_2 + 3 * (y_2 - y_1)
                        break

        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forloc(acord_data, page_no)

    if y_min == 9999:

        acord_dict["LOC #"].append("NULL")
    else:

        def get_bounds_loc(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):
                        acord_dict["LOC #"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_loc(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["LOC #"]) == 0:
            acord_dict["LOC #"].append("NULL")
    
    

    def get_bounds_forcity(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= yprem_max and y_2 <= 1.5 * \
                        ymin_op[0] and x_2 < xmin_op[0]:
                    if trial == "CITY":
                        y_street1=y_1
                        y_min = y_1 - 6
                        x_max = x_2 + 9 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 10
                        break

        except Exception as _:
            pass
        
        try:
            y_street1
        
        except:
            y_street1=y_max
        return y_min, x_min, y_max, x_max,y_street1

    y_min, x_min, y_max, x_max,y_street1 = get_bounds_forcity(acord_data, page_no)

    if y_min == 9999:
        acord_dict["CITY"].append("NULL")
    else:
        new_list = []

        def get_bounds_city(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):
                        new_list.append(trial)
            except Exception as _:
                pass
            return trial

        _ = get_bounds_city(acord_data, page_no, y_min, x_min, y_max, x_max)

        if len(new_list) == 0:

            acord_dict["CITY"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                acord125 = " ".join(new_list)

                acord_dict["CITY"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["CITY"].append(acord125)

    # for county
    def get_bounds_forcounty(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= yprem_max and y_2 <= 1.5 * ymin_op[0]:
                    if trial == "COUNTY":
                        y_min = y_1 - 10
                        x_max = x_2 + 5 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 5
                        break

        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forcounty(acord_data, page_no)

    if y_min == 9999:
        acord_dict["COUNTY"].append("NULL")
    else:
        new_list = []

        def get_bounds_county(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_max,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):
                        new_list.append(trial)
            except Exception as _:
                pass
            return trial

        _ = get_bounds_county(acord_data, page_no, y_min, x_min, y_max, x_max)

        if len(new_list) == 0:

            acord_dict["COUNTY"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                acord125 = " ".join(new_list)

                acord_dict["COUNTY"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["COUNTY"].append(acord125)

    # for zip
    def get_bounds_forzip(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= yprem_max and y_2 <= 1.5 * ymin_op[0]:
                    if trial == "ZIP":
                        y_min = y_1 - 6
                        x_max = x_2 + 6.5 * (x_2 - x_1)
                        x_min = x_2 + 7.5
                        y_max = y_2 + 5
                        break

        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forzip(acord_data, page_no)

    if y_min == 9999:

        acord_dict["ZIP"].append("NULL")
    else:

        def get_bounds_zip(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:

                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["ZIP"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_zip(acord_data, page_no, y_min, x_min, y_max, x_max)

        if len(acord_dict["ZIP"]) == 0:
            # if zips == "4":
            acord_dict["ZIP"].append("NULL")

    def get_bounds_forstreet(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= yprem_max and y_2 <= ymin_op[0]:
                    if trial == "STREET":
                        y_min = y_1 - 10
                        x_max = x_2 + 7 * (x_2 - x_1)
                        x_min = x_1 - 12
                        y_max = y_2 + 3.5 * (y_2 - y_1)
                        break

        except Exception as _:
            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forstreet(acord_data, page_no)

    if y_min == 9999:

        acord_dict["STREET"].append("NULL")
    else:

        new_list = []

        def get_bounds_street(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_street1,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_street1):

                        new_list.append(trial)
            except Exception as _:

                pass
            return trial

        _ = get_bounds_street(acord_data, page_no, y_min, x_min, y_street1, x_max)

        if len(new_list) == 0:

            acord_dict["STREET"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                if len(new_list) == 0:

                    acord_dict["STREET"].append("NULL")
                else:
                    if "STREET" in new_list:
                        new_list.remove("STREET")
                        if len(new_list) == 0:

                            acord_dict["STREET"].append("NULL")
                        else:
                            acord125 = " ".join(new_list)

                            acord_dict["STREET"].append(acord125)
                    else:
                        acord125 = " ".join(new_list)

                        acord_dict["STREET"].append(acord125)

            else:
                if "STREET" in new_list:
                    new_list.remove("STREET")
                    if len(new_list) == 0:

                        acord_dict["STREET"].append("NULL")
                    else:
                        acord125 = " ".join(new_list)

                        acord_dict["STREET"].append(acord125)
                else:
                    acord125 = " ".join(new_list)

                    acord_dict["STREET"].append(acord125)

    # for state
    def get_bounds_forstate(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= yprem_max and y_2 <= ymin_op[0]:
                    if trial == "STATE":

                        y_min = y_1 - (y_2 - y_1)
                        x_max = x_2 + 1.5 * (x_2 - x_1)
                        x_min = x_2 + 5
                        y_max = y_2 + 10
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forstate(acord_data, page_no)

    if y_min == 9999:

        acord_dict["STATE"].append("NULL")
    else:

        def get_bounds_state(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["STATE"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_state(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["STATE"]) == 0:
            # if state == "4":
            acord_dict["STATE"].append("NULL")

    def get_bounds_fordescriptionofoperations2(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[0] and y_2 <= (
                    ymax_op[0] + 1.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "OPERATIONS":

                        y_min = y_1 - 20
                        x_max = x_2 + 8.5 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 20
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_fordescriptionofoperations2(
        acord_data, page_no
    )

    if y_min == 9999:

        acord_dict["DESCRIPTION OF OPERATIONS"].append("NULL")
    else:
        new_list = []

        def get_bounds_descriptionofoperations2(
            acord_data, page_no, y_min, x_min, y_max, x_max
        ):
            """
            Function to get the Boundary values for Physical Address
            """

            try:

                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        new_list.append(trial)
            except Exception as _:

                pass
            return trial

        _ = get_bounds_descriptionofoperations2(
            acord_data, page_no, y_min, x_min, y_max, x_max
        )

        if len(new_list) == 0:

            acord_dict["DESCRIPTION OF OPERATIONS"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                acord125 = " ".join(new_list)

                acord_dict["DESCRIPTION OF OPERATIONS"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["DESCRIPTION OF OPERATIONS"].append(acord125)

    

    def get_bounds_forbld2(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)

                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[0] and y_2 <= (
                    ymax_op[0] + 1.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "BLD":
                        y_min = y_2
                        x_max = x_2 + 20
                        x_min = x_1 - 5
                        y_max = y_2 + 3.5 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forbld2(acord_data, page_no)

    if y_min == 9999:

        acord_dict["BLD #"].append("NULL")
    else:

        def get_bounds_bld2(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["BLD #"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_bld2(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["BLD #"]) == 1:
            # if bld2 == "4":
            acord_dict["BLD #"].append("NULL")
    
    
    
    def get_bounds_forloc2(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[0] and y_2 <= (
                    ymax_op[0] + 1.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "LOC":

                        y_min = y_2
                        x_max = x_2 + 20
                        x_min = x_1 - 5
                        y_max = y_2 + 3 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forloc2(acord_data, page_no)

    if y_min == 9999:

        acord_dict["LOC #"].append("NULL")
    else:

        def get_bounds_loc2(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["LOC #"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_loc2(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["LOC #"]) == 1:
            # if loc2 == "4":
            acord_dict["LOC #"].append("NULL")
    

    def get_bounds_forcity2(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if (
                    y_1 >= ymax_op[0]
                    and y_2 <= (ymax_op[0] + 1.5 * (ymin_op[0] - yprem_max))
                    and x_2 < xmin_op[0]
                ):
                    if trial == "CITY":
                        y_street2 = y_1
                        y_min = y_1 - 6
                        x_max = x_2 + 9 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 5
                        break

        except Exception as _:

            pass
        try:
            y_street2
        except:
            y_street2=y_max
        return y_min, x_min, y_max, x_max, y_street2

    y_min, x_min, y_max, x_max, y_street2 = get_bounds_forcity2(acord_data, page_no)

    if y_min == 9999:

        acord_dict["CITY"].append("NULL")
    else:

        new_list = []

        def get_bounds_city2(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        new_list.append(trial)
            except Exception as _:

                pass
            return trial

        _ = get_bounds_city2(acord_data, page_no, y_min, x_min, y_max, x_max)

        if len(new_list) == 0:

            acord_dict["CITY"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                acord125 = " ".join(new_list)

                acord_dict["CITY"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["CITY"].append(acord125)

    # for county
    def get_bounds_forcounty2(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[0] and y_2 <= (
                    ymax_op[0] + 1.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "COUNTY":

                        y_min = y_1 - 5
                        x_max = x_2 + 5 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 5
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forcounty2(acord_data, page_no)

    if y_min == 9999:

        acord_dict["COUNTY"].append("NULL")
    else:

        new_list = []

        def get_bounds_county2(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_max,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        new_list.append(trial)
                        # break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_county2(
            acord_data,
            page_no,
            y_min,
            x_min,
            y_max,
            x_max)

        if len(new_list) == 0:

            acord_dict["COUNTY"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                acord125 = " ".join(new_list)

                acord_dict["COUNTY"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["COUNTY"].append(acord125)

    # for zip
    def get_bounds_forzip2(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[0] and y_2 <= (
                    ymax_op[0] + 1.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "ZIP":
                        y_min = y_1 - 6
                        x_max = x_2 + 6.5 * (x_2 - x_1)
                        x_min = x_2 + 7.5
                        y_max = y_2 + 5
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forzip2(acord_data, page_no)

    if y_min == 9999:

        acord_dict["ZIP"].append("NULL")
    else:

        def get_bounds_zip2(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["ZIP"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_zip2(acord_data, page_no, y_min, x_min, y_max, x_max)

        if len(acord_dict["ZIP"]) == 1:
            # if zip2 == "4":
            acord_dict["ZIP"].append("NULL")

    # for street
    def get_bounds_forstreet2(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[0] and y_2 <= (
                    ymax_op[0] + 1.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "STREET":

                        y_min = y_1 - 10
                        x_max = x_2 + 7 * (x_2 - x_1)
                        x_min = x_1 - 12
                        y_max = y_2 + 3.5 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forstreet2(acord_data, page_no)

    if y_min == 9999:

        acord_dict["STREET"].append("NULL")
    else:

        new_list = []

        def get_bounds_street2(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_street2,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    # try:
                    #     y_street2
                    # except:
                    #     y_street2=y_max
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_street2):

                        new_list.append(trial)
                        # break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_street2(
            acord_data,
            page_no,
            y_min,
            x_min,
            y_street2,
            x_max)

        if len(new_list) == 0:

            acord_dict["STREET"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                if len(new_list) == 0:

                    acord_dict["STREET"].append("NULL")
                else:
                    if "STREET" in new_list:
                        new_list.remove("STREET")
                        if len(new_list) == 0:

                            acord_dict["STREET"].append("NULL")
                        else:
                            acord125 = " ".join(new_list)

                            acord_dict["STREET"].append(acord125)
                    else:
                        acord125 = " ".join(new_list)

                        acord_dict["STREET"].append(acord125)

            else:
                if "STREET" in new_list:
                    new_list.remove("STREET")
                    if len(new_list) == 0:

                        acord_dict["STREET"].append("NULL")
                    else:
                        acord125 = " ".join(new_list)

                        acord_dict["STREET"].append(acord125)
                else:
                    acord125 = " ".join(new_list)

                    acord_dict["STREET"].append(acord125)

    # for state
    def get_bounds_forstate2(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[0] and y_2 <= (
                    ymax_op[0] + 1.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "STATE":

                        y_min = y_1 - (y_2 - y_1)
                        x_max = x_2 + 1.5 * (x_2 - x_1)
                        x_min = x_2 + 5
                        y_max = y_2 + 10
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forstate2(acord_data, page_no)

    if y_min == 9999:

        acord_dict["STATE"].append("NULL")
    else:

        def get_bounds_state2(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_max,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["STATE"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_state2(acord_data, page_no, y_min, x_min, y_max, x_max)

        if len(acord_dict["STATE"]) == 1:
            # if state2 == "4":
            acord_dict["STATE"].append("NULL")
    # Table3

    def get_bounds_fordescriptionofoperations3(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[1] and y_2 <= (
                    ymax_op[0] + 2.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "OPERATIONS":

                        y_min = y_1 - 20
                        x_max = x_2 + 8.5 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 20
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_fordescriptionofoperations3(
        acord_data, page_no
    )

    if y_min == 9999:

        acord_dict["DESCRIPTION OF OPERATIONS"].append("NULL")
    else:
        new_list = []

        def get_bounds_descriptionofoperations3(
            acord_data, page_no, y_min, x_min, y_max, x_max
        ):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        new_list.append(trial)
            except Exception as _:

                pass
            return trial

        _ = get_bounds_descriptionofoperations3(
            acord_data, page_no, y_min, x_min, y_max, x_max
        )
        if len(new_list) == 0:

            acord_dict["DESCRIPTION OF OPERATIONS"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                acord125 = " ".join(new_list)

                acord_dict["DESCRIPTION OF OPERATIONS"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["DESCRIPTION OF OPERATIONS"].append(acord125)

    

    def get_bounds_forbld3(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)

                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[1] and y_2 <= (
                    ymax_op[0] + 2.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "BLD":
                        y_min = y_2
                        x_max = x_2 + 20
                        x_min = x_1 - 5
                        y_max = y_2 + 3.5 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forbld3(acord_data, page_no)

    if y_min == 9999:

        acord_dict["BLD #"].append("NULL")
    else:

        def get_bounds_bld3(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["BLD #"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_bld3(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["BLD #"]) == 2:
            # if bld3 == "4":
            acord_dict["BLD #"].append("NULL")
            
            
    
    def get_bounds_forloc3(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[1] and y_2 <= (
                    ymax_op[0] + 2.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "LOC":
                        y_min = y_2
                        x_max = x_2 + 20
                        x_min = x_1 - 5
                        y_max = y_2 + 3 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forloc3(acord_data, page_no)

    if y_min == 9999:

        acord_dict["LOC #"].append("NULL")
    else:

        def get_bounds_loc3(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:

                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["LOC #"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_loc3(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["LOC #"]) == 2:
            # if loc3 == "4":
            acord_dict["LOC #"].append("NULL")
    
    

    def get_bounds_forcity3(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if (
                    y_1 >= ymax_op[1]
                    and y_2 <= (ymax_op[0] + 2.5 * (ymin_op[0] - yprem_max))
                    and x_2 < xmin_op[0]
                ):
                    if trial == "CITY":
                        y_street3 = y_1
                        y_min = y_1 - (y_2 - y_1)
                        x_max = x_2 + 9 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 4
                        break

        except Exception as _:

            pass
        
        try:
            y_street3
        except:
            y_street3=y_max
        return y_min, x_min, y_max, x_max, y_street3

    y_min, x_min, y_max, x_max, y_street3 = get_bounds_forcity3(acord_data, page_no)

    if y_min == 9999:

        acord_dict["CITY"].append("NULL")
    else:

        new_list = []

        def get_bounds_city3(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        new_list.append(trial)
            except Exception as _:

                pass
            return trial

        _ = get_bounds_city3(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(new_list) == 0:

            acord_dict["CITY"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                acord125 = " ".join(new_list)

                acord_dict["CITY"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["CITY"].append(acord125)

    # for county
    def get_bounds_forcounty3(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[1] and y_2 <= (
                    ymax_op[0] + 2.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "COUNTY":

                        y_min = y_1 - 5
                        x_max = x_2 + 5 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 2
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forcounty3(acord_data, page_no)

    if y_min == 9999:

        acord_dict["COUNTY"].append("NULL")
    else:

        new_list = []

        def get_bounds_county3(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_max,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        new_list.append(trial)
                        # break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_county3(
            acord_data,
            page_no,
            y_min,
            x_min,
            y_max,
            x_max)
        if len(new_list) == 0:

            acord_dict["COUNTY"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                acord125 = " ".join(new_list)

                acord_dict["COUNTY"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["COUNTY"].append(acord125)

    # for zip
    def get_bounds_forzip3(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[1] and y_2 <= (
                    ymax_op[0] + 2.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "ZIP":

                        y_min = y_1 - (y_2 - y_1)
                        x_max = x_2 + 6.5 * (x_2 - x_1)
                        x_min = x_2 + 7
                        y_max = y_2 + 10
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forzip3(acord_data, page_no)

    if y_min == 9999:

        acord_dict["ZIP"].append("NULL")
    else:

        def get_bounds_zip3(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["ZIP"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_zip3(acord_data, page_no, y_min, x_min, y_max, x_max)

        if len(acord_dict["ZIP"]) == 2:
            # if zip3 == "4":
            acord_dict["ZIP"].append("NULL")

    # for street
    def get_bounds_forstreet3(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[1] and y_2 <= (
                    ymax_op[0] + 2.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "STREET":

                        y_min = y_1 - 10
                        x_max = x_2 + 7 * (x_2 - x_1)
                        x_min = x_1 - 12
                        y_max = y_2 + 3.5 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forstreet3(acord_data, page_no)

    if y_min == 9999:

        acord_dict["STREET"].append("NULL")
    else:

        new_list = []

        def get_bounds_street3(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_street3,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_street3):

                        new_list.append(trial)
                        # break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_street3(
            acord_data,
            page_no,
            y_min,
            x_min,
            y_street3,
            x_max)
        if len(new_list) == 0:

            acord_dict["STREET"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                if len(new_list) == 0:

                    acord_dict["STREET"].append("NULL")
                else:
                    if "STREET" in new_list:
                        new_list.remove("STREET")
                        if len(new_list) == 0:

                            acord_dict["STREET"].append("NULL")
                        else:
                            acord125 = " ".join(new_list)

                            acord_dict["STREET"].append(acord125)
                    else:
                        acord125 = " ".join(new_list)

                        acord_dict["STREET"].append(acord125)

            else:
                if "STREET" in new_list:
                    new_list.remove("STREET")
                    if len(new_list) == 0:

                        acord_dict["STREET"].append("NULL")
                    else:
                        acord125 = " ".join(new_list)

                        acord_dict["STREET"].append(acord125)
                else:
                    acord125 = " ".join(new_list)

                    acord_dict["STREET"].append(acord125)

    # for state

    def get_bounds_forstate3(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[1] and y_2 <= (
                    ymax_op[0] + 2.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "STATE":

                        y_min = y_1 - (y_2 - y_1)
                        x_max = x_2 + 1.5 * (x_2 - x_1)
                        x_min = x_2 + 5
                        y_max = y_2 + 10
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forstate3(acord_data, page_no)

    if y_min == 9999:

        acord_dict["STATE"].append("NULL")
    else:

        def get_bounds_state3(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_max,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["STATE"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_state3(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["STATE"]) == 2:
            # if state3 == "4":
            acord_dict["STATE"].append("NULL")
    # table4

    def get_bounds_fordescriptionofoperations4(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[2] and y_2 <= (
                    ymax_op[0] + 3.8 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "OPERATIONS":

                        y_min = y_1 - 20
                        x_max = x_2 + 8.5 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 20
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_fordescriptionofoperations4(
        acord_data, page_no
    )

    if y_min == 9999:

        acord_dict["DESCRIPTION OF OPERATIONS"].append("NULL")
    else:
        new_list = []

        def get_bounds_descriptionofoperations4(
            acord_data, page_no, y_min, x_min, y_max, x_max
        ):
            """
            Function to get the Boundary values for Physical Address
            """

            try:

                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        new_list.append(trial)
            except Exception as _:

                pass
            return trial

        _ = get_bounds_descriptionofoperations4(
            acord_data, page_no, y_min, x_min, y_max, x_max
        )
        if len(new_list) == 0:

            acord_dict["DESCRIPTION OF OPERATIONS"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                acord125 = " ".join(new_list)

                acord_dict["DESCRIPTION OF OPERATIONS"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["DESCRIPTION OF OPERATIONS"].append(acord125)

    

    def get_bounds_forbld4(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)

                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[2] and y_2 <= (
                    ymax_op[0] + 3.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "BLD":
                        y_min = y_2
                        x_max = x_2 + 20
                        x_min = x_1 - 5
                        y_max = y_2 + 3.5 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forbld4(acord_data, page_no)

    if y_min == 9999:

        acord_dict["BLD #"].append("NULL")
    else:

        def get_bounds_bld4(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["BLD #"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_bld4(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["BLD #"]) == 3:
            # if bld4 == "4":
            acord_dict["BLD #"].append("NULL")
    
    
    
    def get_bounds_forloc4(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)

                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[2] and y_2 <= (
                    ymax_op[0] + 3.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "LOC":

                        y_min = y_2
                        x_max = x_2 + 20
                        x_min = x_1 - 5
                        y_max = y_2 + 3 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forloc4(acord_data, page_no)

    if y_min == 9999:

        acord_dict["LOC #"].append("NULL")
    else:

        def get_bounds_loc4(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)
                
                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["LOC #"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_loc4(acord_data, page_no, y_min, x_min,y_max, x_max)

        if len(acord_dict["LOC #"]) == 3:

            # if loc4 == "4":
            acord_dict["LOC #"].append("NULL")
    
    
    def get_bounds_forcity4(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if (
                    y_1 >= ymax_op[2]
                    and y_2 <= (ymax_op[0] + 3.5 * (ymin_op[0] - yprem_max))
                    and x_2 < xmin_op[0]
                ):
                    if trial == "CITY":
                        y_street4 = y_1
                        y_min = y_1 - (y_2 - y_1)
                        x_max = x_2 + 9 * (x_2 - x_1)
                        x_min = x_2 + 4
                        y_max = y_2 + 4
                        break

        except Exception as _:

            pass
        
        try:
            y_street4
        except:
            y_street4=y_max
        return y_min, x_min, y_max, x_max, y_street4

    y_min, x_min, y_max, x_max, y_street4 = get_bounds_forcity4(acord_data, page_no)

    if y_min == 9999:

        acord_dict["CITY"].append("NULL")
    else:

        new_list = []

        def get_bounds_city4(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        new_list.append(trial)
            except Exception as _:

                pass
            return trial

        _ = get_bounds_city4(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(new_list) == 0:

            acord_dict["CITY"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                if len(new_list) == 0:

                    acord_dict["CITY"].append("NULL")
                else:
                    acord125 = " ".join(new_list)

                    acord_dict["CITY"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["CITY"].append(acord125)

    # for county
    def get_bounds_forcounty4(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[2] and y_2 <= (
                    ymax_op[0] + 3.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "COUNTY":

                        y_min = y_1 - 5
                        x_max = x_2 + 5 * (x_2 - x_1)
                        x_min = x_2 + 2
                        y_max = y_2 + 2
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forcounty4(acord_data, page_no)

    if y_min == 9999:

        acord_dict["COUNTY"].append("NULL")
    else:

        new_list = []

        def get_bounds_county4(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_max,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:

                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        new_list.append(trial)
                        # break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_county4(
            acord_data,
            page_no,
            y_min,
            x_min,
            y_max,
            x_max)

        if len(new_list) == 0:

            acord_dict["COUNTY"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                if len(new_list) == 0:

                    acord_dict["COUNTY"].append("NULL")
                else:
                    acord125 = " ".join(new_list)

                    acord_dict["COUNTY"].append(acord125)
            else:
                acord125 = " ".join(new_list)

                acord_dict["COUNTY"].append(acord125)

    # for zip
    def get_bounds_forzip4(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[2] and y_2 <= (
                    ymax_op[0] + 3.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "ZIP":

                        y_min = y_1 - (y_2 - y_1)
                        x_max = x_2 + 6.5 * (x_2 - x_1)
                        x_min = x_2 + 7.5
                        y_max = y_2 + 10
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forzip4(acord_data, page_no)

    if y_min == 9999:

        acord_dict["ZIP"].append("NULL")
    else:

        def get_bounds_zip4(acord_data, page_no, y_min, x_min, y_max, x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:
                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["ZIP"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_zip4(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["ZIP"]) == 3:
            # if zip4 == "4":
            acord_dict["ZIP"].append("NULL")

    # for street
    def get_bounds_forstreet4(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)
                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[2] and y_2 <= (
                    ymax_op[0] + 3.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "STREET":

                        y_min = y_1 - 10
                        x_max = x_2 + 7 * (x_2 - x_1)
                        x_min = x_1 - 12
                        y_max = y_2 + 3.5 * (y_2 - y_1)
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forstreet4(acord_data, page_no)

    if y_min == 9999:

        acord_dict["STREET"].append("NULL")
    else:

        new_list = []

        def get_bounds_street4(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_street4,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:

                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_street4):

                        new_list.append(trial)
            except Exception as _:

                pass
            return trial

        _ = get_bounds_street4(
            acord_data,
            page_no,
            y_min,
            x_min,
            y_street4,
            x_max)
        if len(new_list) == 0:

            acord_dict["STREET"].append("NULL")
        else:
            if ":" in new_list:
                new_list.remove(":")
                if len(new_list) == 0:

                    acord_dict["STREET"].append("NULL")
                else:
                    if "STREET" in new_list:
                        new_list.remove("STREET")
                        if len(new_list) == 0:

                            acord_dict["STREET"].append("NULL")
                        else:
                            acord125 = " ".join(new_list)

                            acord_dict["STREET"].append(acord125)
                    else:
                        acord125 = " ".join(new_list)

                        acord_dict["STREET"].append(acord125)

            else:
                if "STREET" in new_list:
                    new_list.remove("STREET")
                    if len(new_list) == 0:

                        acord_dict["STREET"].append("NULL")
                    else:
                        acord125 = " ".join(new_list)

                        acord_dict["STREET"].append(acord125)
                else:
                    acord125 = " ".join(new_list)

                    acord_dict["STREET"].append(acord125)

    # for state
    def get_bounds_forstate4(acord_data, page_no):
        """
        Function to get the Boundary values for Physical Address
        """
        try:
            y_min = 9999
            y_max = -9999
            x_min = 9999
            x_max = -9999
            for token in acord_data["pages"][page_no]["tokens"]:
                f_text = _get_text(acord_data, token, element_type="tokens")
                # f_text = f_text.lower()
                trial = re.sub(r"[\n\t\s]*", "", f_text)

                x_1, x_2 = get_x_coordinates(token)
                y_1, y_2 = get_y_coordinates(token)
                if y_1 >= ymax_op[2] and y_2 <= (
                    ymax_op[0] + 3.5 * (ymin_op[0] - yprem_max)
                ):
                    if trial == "STATE":

                        y_min = y_1 - (y_2 - y_1)
                        x_max = x_2 + 1.5 * (x_2 - x_1)
                        x_min = x_2 + 5
                        y_max = y_2 + 10
                        break

        except Exception as _:

            pass
        return y_min, x_min, y_max, x_max

    y_min, x_min, y_max, x_max = get_bounds_forstate4(acord_data, page_no)

    if y_min == 9999:

        acord_dict["STATE"].append("NULL")
    else:

        def get_bounds_state4(
                acord_data,
                page_no,
                y_min,
                x_min,
                y_max,
                x_max):
            """
            Function to get the Boundary values for Physical Address
            """

            try:

                for token in acord_data["pages"][page_no]["tokens"]:
                    f_text = _get_text(
                        acord_data, token, element_type="tokens")
                    # f_text = f_text.lower()
                    trial = re.sub(r"[\n\t\s]*", "", f_text)
                    x_1, x_2 = get_x_coordinates(token)
                    y_1, y_2 = get_y_coordinates(token)

                    if (x_min < x_1 < x_2 < x_max) and (
                            y_min < y_1 < y_2 < y_max):

                        acord_dict["STATE"].append(trial)
                        break
            except Exception as _:

                pass
            return trial

        _ = get_bounds_state4(acord_data, page_no, y_min, x_min, y_max, x_max)
        if len(acord_dict["STATE"]) == 3:
            # if state4 == "4":
            acord_dict["STATE"].append("NULL")
    # acord_dict["PageNumber"] = page_no
    return acord_dict


def page_number(page_no, acord_data):
    """
    Check The current Page Number of the Form
    """
    flag = -999
    mark = -999
    flag_new = -999
    second_count = -999
    new_count = -999
    add = []
    for count, token in enumerate(acord_data["pages"][page_no]["tokens"]):
        f_text = _get_text(acord_data, token, element_type="tokens")
        # f_text = f_text.lower()
        _, _ = get_x_coordinates(token)  # x_1, x_2
        _, _ = get_y_coordinates(token)

        trial = re.sub(r"[\n\t\s]*", "", f_text)
        
        if trial== "BOILER":
            flag = count
        if trial == "MACHINERY":
            if count < flag+4:
                add.append(4)

#         if trial == "APPLICANT":  # "BOILER": #"SECTIONS":
#             flag = count
#         if trial == "INFORMATION":  # "MACHINERY": #"ATTACHED":
#             if count < flag+4:
                # add.append(4)
    
        if trial == "NATURE":
            mark = count
        if trial == "BUSINESS":
            if count < mark + 10:
                add.append(0)
                
    return add, page_no


def final_dict(acord125, acord125_dict, policy):
    """
    Function combines two dictionaries into a dataframe
    """
    new_dict = dict(list(acord125.items()) + list(acord125_dict.items()))
    df_acord = pd.DataFrame([new_dict])
    df_acord["Policy#"] = policy
    df_acord = df_acord.apply(pd.Series.explode).reset_index(drop=True)
    first_column = df_acord.pop("Policy#")
    df_acord.insert(0, "Policy#", first_column)
    df_acord = df_acord.dropna(how='all',
                                 subset=['LOC #', 'BLD #'])
    # df_acord = df_acord[[df_acord['LOC #']!= "NULL"] and [df_acord['LOC
    # #']!= "NULL"]]
    df_acord.drop(df_acord.loc[df_acord['LOC #']
                   == "NULL"].index, inplace=True)
    df_acord.rename(
        columns={
            "Policy#": "POLICY_NO",
            "PROPOSED EFF DATE": "ACORD_EFF_DATE",
            "PROPOSED EXP DATE": "ACORD_EXP_DATE",
            "DESCRIPTION OF OPERATIONS": "DESCRIPTION_OF_OPERATIONS",
            "LOC #": "ACORD_PREM_NO",
            "BLD #": "ACORD_BLDG_NO",
            "CITY": "ACORD_CITY",
            "COUNTY": "ACORD_COUNTY",
            "ZIP": "ACORD_ZIP",
            "STREET": "ACORD_STREET_ADDRESS",
            "STATE": "ACORD_STATE"
        },
        inplace=True,
    )
    return df_acord


def acord_main(document_obj, pdf_name,results):
    """
    Main Function to extract results of ACORD125
    """
    try:
        results=results
        json_string = proto.Message.to_json(document_obj)
        acord_data = json.loads(json_string)
        # acord_data = json_obj(document_obj)
        pdf_list = pdf_name.split(".")
        pdf_wo_ext = pdf_list[0]
        pdf_wo_policy = (pdf_wo_ext.split(" "))[0]
        acord125 = {}
        acord125_dict = {}
        for item in range(len(acord_data["pages"])):

            page_no = item
            add, page = page_number(page_no, acord_data)

            if 4 in add:

                _ = page + 1
                acord125 = acord_125_page1(acord_data, page_no)

            elif 0 in add:
                _ = page + 1
                acord125_dict = acord_125_page2(acord_data, page_no)
        if len(acord125.keys()) == 0:
            acord125["PROPOSED EFF DATE"] = "NULL"
            acord125["PROPOSED EXP DATE"] = "NULL"

        if len(acord125_dict.keys()) == 0:
            acord125_dict["DESCRIPTION OF OPERATIONS"] = "NULL"
            acord125_dict["LOC #"] = "NULL"
            acord125_dict["BLD #"] = "NULL"
            acord125_dict["CITY"] = "NULL"
            acord125_dict["COUNTY"] = "NULL"
            acord125_dict["ZIP"] = "NULL"
            acord125_dict["STREET"] = "NULL"
            acord125_dict["STATE"] = "NULL"
        # policy number name to be extracted from form parse object name
        df_acord = final_dict(acord125, acord125_dict, pdf_wo_policy)
        if df_acord.empty:
            df_acord = pd.DataFrame()
            df_acord = df_acord.append({
                "POLICY_NO": pdf_wo_policy,
                "ACORD_EFF_DATE": " ",
                "ACORD_EXP_DATE": " ",
                "DESCRIPTION_OF_OPERATIONS": " ",
                "ACORD_PREM_NO": " ",
                "ACORD_BLDG_NO": " ",
                "ACORD_CITY": " ",
                "ACORD_COUNTY": " ",
                "ACORD_ZIP": " ",
                "ACORD_STREET_ADDRESS": " ",
                "ACORD_STATE": " "}, ignore_index=True)

        df_acord.to_csv(f"{pdf_wo_ext}.csv", index=False)
        #print(df_acord)
        df_acord.to_gbq(
            destination_table=TABLE,
            project_id=PROJECT_ID,
            chunksize=10000,
            if_exists="append",
        )
        storage_client = storage.Client()
        storage_client.get_bucket(BUCKET_NAME).blob(
            "Application/Import/" +
            pdf_wo_policy +
            '.csv').upload_from_string(
            df_acord.to_csv(),
            'text/csv')

        return df_acord, "success", 200
    except:
        print(str(traceback.format_exc()),"********** Failed in accord Document **********")
        return {"error": str(traceback.format_exc())}, 'failed', 500
