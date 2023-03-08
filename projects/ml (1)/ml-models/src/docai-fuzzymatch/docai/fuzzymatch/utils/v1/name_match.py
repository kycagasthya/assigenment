# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
""" name_match to calculate fuzzy name match score entities from parsrs """
import sys
import traceback
from .helpers import Helper
from .rule_name import RuleConstants
from .constant import Constant
from qdocai.logger import QDocLogger
from qdocai.utils import DocAIBase,DocAIException
from docai.fuzzymatch.utils.v1 import error_code


class FuzzyNameMatch(Helper,DocAIBase):
    """
    class to fuzzy match the predicted values
    from doc parser with true values
    """
    def __init__(
        self,
        request_id: str="",
        page_id:int = 1
    ):
        self.request_id=request_id
        self.page_id=page_id
        self.logger = QDocLogger()
        self.error_dict = error_code.Errors.error_codes
        DocAIBase.__init__(self, request_id=request_id, page_id=page_id)

    def clean_output(self, inp_entity: str) -> str:
        """
        This method is used to call clean text
        from helper.py
        Arguments:
            inp_entity (str):input name
        Returns:
            inp_entity(str): cleaned string
        """
        try:
            inp_entity = self.cleantext(inp_entity)
            return inp_entity
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-processor",
                message=self.error_dict["ERROR_NAME_MATCH"]["text_desc"],
                status_code=self.error_dict["ERROR_NAME_MATCH"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="Invalid Name",
                message=self.error_dict[
                    "ERROR_NAME_MATCH"]["text_desc"],
                status_desc=self.error_dict["ERROR_NAME_MATCH"]["desc"],
                status_code=self.error_dict["ERROR_NAME_MATCH"]["code"],
            )from error


    def fuzzy_name_match(self, real_name: str, pred_name: str)->dict:
        """
        This method is used to fuzzymatch two names
        does the rule base macth and calculates fuzzy
        score only in condition of no match
        Arguments:
            real_name (str):input name
            pred_name (str):pred name
        Returns:
            result_dict (dict): actuals,match score
        """
        try:
            result_dict = {}
            self.logger.ml_logger(
                level="INFO",
                ml_package="docai-fuzzymatch",
                action="Fuzzy Name Match",
                status_code=200,
                message="Real Name -->{} and"
                        " Pred Name --> {}",
                request_id=self.request_id,
                page_id=self.page_id
            )
            pred_name = self.clean_output(pred_name)
            real_name = self.clean_output(real_name)
            pred_name_array = pred_name.split(" ")
            real_name_array = real_name.split(" ")
            if(len(real_name.strip())<=1
              or len(pred_name.strip())<=1):
                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = float(0)
                result_dict["matchingType"] = RuleConstants.RULE0
                return result_dict


            if (
                real_name==pred_name
                and len(real_name_array)>1
                and len(pred_name_array)>1
            ) :
                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = float(1)
                result_dict["matchingType"] = RuleConstants.RULE1
                return result_dict

            elif (
                real_name == pred_name
                and len(real_name_array)==1
                and len(pred_name_array)==1
            ):
                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = float(1)
                result_dict["matchingType"] = RuleConstants.RULE2
                return result_dict

            elif (
                len(real_name_array[0])<=1
            ):
                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = self.cal_fuzz_score(
                    real_name,pred_name)
                result_dict["matchingType"] = RuleConstants.RULE0
                return result_dict

            elif (
                len(real_name_array)==2
                and len(pred_name_array)==2
                and real_name_array[0]==pred_name_array[1]
                and real_name_array[1]==pred_name_array[0]

            ):
                result_dict[
                        "real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = float(1)
                result_dict["matchingType"] = RuleConstants.RULE3
                return result_dict

            elif (
                len(real_name_array)>2
                and len(pred_name_array)>2
                and real_name_array[0]==pred_name_array[1]
                and real_name_array[-1]==pred_name_array[0]

            ):
                middle_real = real_name_array[1:len(real_name_array)-1]
                middle_pred = pred_name_array[2:]
                score = self.cal_fuzz_score(middle_real,middle_pred)
                if score>Constant.FUZZY_MATCH_THRESH:
                    result_dict[
                            "real_name"] = real_name
                    result_dict["pred_name"] = pred_name
                    result_dict["matchingScore"] = float(1)
                    result_dict["matchingType"] = RuleConstants.RULE3
                    return result_dict
                else:
                    result_dict[
                            "real_name"] = real_name
                    result_dict["pred_name"] = pred_name
                    result_dict["matchingScore"] = score
                    result_dict["matchingType"] = RuleConstants.RULE0
                    return result_dict


            elif (
                len(real_name_array)>2
                and len(pred_name_array)>2
                and real_name_array[0]==pred_name_array[0]
                and real_name_array[-1]==pred_name_array[1]
                and len(real_name_array[-1])>1
                and len(pred_name_array[-1])>1

            ):
                middle_real = real_name_array[1:len(real_name_array)-1]
                middle_pred = pred_name_array[2:]
                score = self.cal_fuzz_score(middle_real,middle_pred)
                if score>Constant.FUZZY_MATCH_THRESH:
                    result_dict[
                            "real_name"] = real_name
                    result_dict["pred_name"] = pred_name
                    result_dict["matchingScore"] = float(1)
                    result_dict["matchingType"] = RuleConstants.RULE3
                    return result_dict
                else:
                    result_dict[
                            "real_name"] = real_name
                    result_dict["pred_name"] = pred_name
                    result_dict["matchingScore"] = score
                    result_dict["matchingType"] = RuleConstants.RULE0
                    return result_dict


            elif (
                len(real_name_array)>2
                and len(pred_name_array)>2
                and len(real_name_array)==len(pred_name_array)
                and real_name_array[0]==pred_name_array[-1]
                and real_name_array[-1]==pred_name_array[0]

            ):
                middle_real = real_name_array[1:len(real_name_array)-1]
                middle_pred = real_name_array[1:len(pred_name_array)-1]
                score = self.cal_fuzz_score(middle_real,middle_pred)
                if score>Constant.FUZZY_MATCH_THRESH:
                    result_dict[
                            "real_name"] = real_name
                    result_dict["pred_name"] = pred_name
                    result_dict["matchingScore"] = float(1)
                    result_dict["matchingType"] = RuleConstants.RULE3
                    return result_dict


            elif (
                (
                len(real_name_array)>=2
                and len(pred_name_array)>=2
                and real_name_array[0]==pred_name_array[0]
                and real_name_array[-1]==pred_name_array[-1]
                )or
                (
                len(real_name_array)>=2
                and len(pred_name_array)>=2
                and real_name_array[0]==pred_name_array[-1]
                and real_name_array[-1]==pred_name_array[0]
                )

            ):
                middle_real = real_name_array[1:len(real_name_array)-1]
                middle_pred = pred_name_array[1:len(pred_name_array)-1]

                if(
                    (
                    (len(real_name_array)<= 2
                    or len(pred_name_array)<= 2)
                    and real_name_array[0]==pred_name_array[0]
                    and real_name_array[-1]==pred_name_array[-1]
                    ) or
                    (
                    (len(real_name_array)<= 2
                    or len(pred_name_array)<= 2)
                    and real_name_array[0]==pred_name_array[-1]
                    and real_name_array[-1]==pred_name_array[0]
                    )

                ):
                    result_dict["real_name"] = real_name
                    result_dict["pred_name"] = pred_name
                    result_dict["matchingScore"] = float(1)
                    result_dict["matchingType"] = RuleConstants.RULE4
                    return result_dict


                if(
                    (len(real_name_array)==len(pred_name_array))
                    and real_name_array[0]==pred_name_array[0]
                    and real_name_array[-1]==pred_name_array[-1]
                ):
                    match_flag = False
                    for idx,val in enumerate(middle_real):
                        if (
                            (len(val)==1
                            or len(middle_pred[idx])==1)
                           ):
                            match_flag = bool(val[0]==middle_pred[idx][0])

                    if match_flag:
                        result_dict["real_name"] = real_name
                        result_dict["pred_name"] = pred_name
                        result_dict["matchingScore"] = float(1)
                        result_dict["matchingType"] = RuleConstants.RULE4
                        return result_dict


                mnames_match_score = self.cal_fuzz_score(
                    middle_real,middle_pred)

                if mnames_match_score > Constant.FUZZY_MATCH_THRESH:
                    result_dict["real_name"] = real_name
                    result_dict["pred_name"] = pred_name
                    result_dict["matchingScore"] = float(1)
                    result_dict["matchingType"] = RuleConstants.RULE4
                    return result_dict
                else:
                    result_dict["real_name"] = real_name
                    result_dict["pred_name"] = pred_name
                    score = self.cal_fuzz_score(real_name,pred_name)
                    result_dict["matchingScore"] = score
                    result_dict["matchingType"] = RuleConstants.RULE0
                    return result_dict

            elif (
                (len(real_name_array)==2
                and len(pred_name_array)==2
                and len(real_name_array[0])>=1)
                and
                ((len(pred_name_array[0])==1
                    and real_name_array[0]==pred_name_array[1]
                     )
                  or(len(pred_name_array[1])==1
                    and real_name_array[0]==pred_name_array[0])
                 or(len(real_name_array[1])==1
                    and len(pred_name_array[1])>1
                    and real_name_array[0]==pred_name_array[0]
                   and real_name_array[1]==pred_name_array[1][0])
                 or(len(real_name_array[1])==1
                    and len(pred_name_array[1])>1
                    and real_name_array[0]==pred_name_array[1]
                   and real_name_array[1]==pred_name_array[0][0])
                )
            ):
                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = float(1)
                result_dict["matchingType"] = RuleConstants.RULE5
                return result_dict


            elif (
                len(real_name_array)>2
                and len(pred_name_array)>2
                and real_name_array[0]==pred_name_array[1]
                and len(pred_name_array[0])==1
                and real_name_array[-1][0]==pred_name_array[0]
                and real_name_array[
                    1:len(real_name_array)-1]==pred_name_array[2:]
            ):
                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = float(1)
                result_dict["matchingType"] = RuleConstants.RULE6
                return result_dict

            elif (
                real_name_array[
                    :len(real_name_array)-1]==pred_name_array[
                    :len(pred_name_array)-1]
                and len(real_name_array[-1])>1
                and real_name_array[-1][0]==pred_name_array[-1]
            ):
                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = float(1)
                result_dict["matchingType"] = RuleConstants.RULE6
                return result_dict

            elif (
                len(real_name_array)==len(pred_name_array)
                and len(real_name_array[0])>1
                and len(pred_name_array[0])>1
                and real_name_array[0]==pred_name_array[0]
            ):
                real_name_array_t = real_name_array[1:]
                pred_name_array_t = pred_name_array[1:]
                for idx,_ in enumerate(real_name_array_t):
                    if real_name_array_t[idx] == pred_name_array_t[idx]:
                        continue
                    elif (
                        len(pred_name_array_t[idx])==1
                        and real_name_array_t[idx][0]==pred_name_array_t[idx]
                    ):
                        continue
                    else:
                        result_dict["real_name"] = real_name
                        result_dict["pred_name"] = pred_name
                        score = self.cal_fuzz_score(real_name,pred_name)
                        result_dict["matchingScore"] = score
                        result_dict["matchingType"] = RuleConstants.RULE0

                        return result_dict


                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = float(1)
                result_dict["matchingType"] = RuleConstants.RULE6
                return result_dict



            elif(
                len(real_name_array)==len(pred_name_array)
                and len(real_name_array)>2
                and len(pred_name_array)>2
                and real_name_array[0]==pred_name_array[1]
                and real_name_array[-1][0]==pred_name_array[0]
            ):
                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                result_dict["matchingScore"] = float(1)
                result_dict["matchingType"] = RuleConstants.RULE6
                return result_dict


            elif(
                len(real_name_array)==len(pred_name_array)
                and len(real_name_array)>2
                and len(pred_name_array)>2
                and len(real_name_array[0])>1
                and real_name_array[-1][0]==pred_name_array[-1][0]
                and real_name_array[0]==pred_name_array[0]
            ):
                mnames_array = real_name_array[1:len(real_name_array)-1]
                single_char_name = False
                for idx,name in enumerate(mnames_array):
                    if len(name)>1:
                        result_dict["real_name"] = real_name
                        result_dict["pred_name"] = pred_name
                        result_dict["matchingScore"] = self.cal_fuzz_score(
                            real_name,pred_name)
                        result_dict["matchingType"] = RuleConstants.RULE0
                        return result_dict

                    else:
                        single_char_name = True
                if single_char_name:
                    result_dict["real_name"] = real_name
                    result_dict["pred_name"] = pred_name
                    result_dict["matchingScore"] = float(1)
                    result_dict["matchingType"] = RuleConstants.RULE6
                    return result_dict

            else:
                result_dict["real_name"] = real_name
                result_dict["pred_name"] = pred_name
                score = self.cal_fuzz_score(real_name,pred_name)
                result_dict["matchingScore"] = score
                result_dict["matchingType"] = RuleConstants.RULE0
                return result_dict

            result_dict["real_name"] = real_name
            result_dict["pred_name"] = pred_name
            score = self.cal_fuzz_score(real_name,pred_name)
            result_dict["matchingScore"] = score
            result_dict["matchingType"] = RuleConstants.RULE0
            return result_dict

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(exc_type,
                                                      exc_value, exc_tb)
            message = "".join(trace_back.format_exception_only())
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-processor",
                message=f"Name Match Failed - {message}",
                status_code=self.error_dict["ERROR_NAME_MATCH"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="Invalid Name values",
                message=f"Name Match Failed - {message}",
                status_desc=self.error_dict["ERROR_NAME_MATCH"]["desc"],
                status_code=self.error_dict["ERROR_NAME_MATCH"]["code"],
            ) from error
