# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
""" address_match to calculate fuzzy name match score entities from parsrs """
from fuzzywuzzy import fuzz
from .helpers import Helper
from .constant import Constant
from typing import Union,Tuple
from .icici_address_split import parse_address
from qdocai.logger import QDocLogger
from qdocai.utils import DocAIBase, DocAIException
from docai.fuzzymatch.utils.v1 import error_code
import sys
import traceback
import re


class AddressMatch(DocAIBase):

    def __init__(
            self,
            request_id: str = "",
            page_id: int = 1,
            all_core_dict = None,
            parser_address: str = ""
    )->None:

        self.addr1 = all_core_dict["addr1"]
        self.addr2 = all_core_dict["addr2"]
        self.addr3 = all_core_dict["addr3"]
        self.addr4 = all_core_dict["addr4"]
        self.city = all_core_dict["city"]
        self.state = all_core_dict["state"]
        self.country = all_core_dict["country"]
        self.pincode = all_core_dict["pincode"]
        self.zipcode = all_core_dict["zipcode"]
        self.parser_address = parser_address
        self.request_id = request_id
        self.page_id = page_id
        self.logger = QDocLogger()
        self.error_dict = error_code.Errors.error_codes
        DocAIBase.__init__(self, request_id=request_id, page_id=page_id)

    def extract_houseno(
            self,
            address: str = ""
    )->Tuple[str,int]:
        """
        extract house no and digits in house no

        Args:
          address(str): inp address as a string

        Returns:
          house_no(str) : extracted house no
          digits(int) : digits from extraxted house no

        Raises:

        """

        address = re.sub(",", " ", address)
        address_list = address.split(" ")
        house_no = ""
        digits = ""

        if "~#" in address:
            house_no = address.split("~#")[0]
        else:
            for val in address_list:
                match = re.match("^[a-zA-Z]+.*[0-9]", val)
                if match is not None:
                    house_no = match.group()
                    break

                match2 = re.match("\\d+", val)
                if match2 is not None:
                    house_no = match2.group()
                    break
        if house_no != "":
            digit = [c for c in house_no if c.isdigit()]
            digits = "".join(digit)

        if house_no == "":
            for val in address_list:
                match = re.search(r"\d+", val)
                if match is not None:
                    house_no = match.group()
                    break
            digit = [c for c in house_no if c.isdigit()]
            digits = "".join(digit)
        if digits == "":
            return house_no, None
        return house_no, digits


    def get_icici_address_splitter(
            self,
            parser_address:str
        )->dict:

        """
        This method is used to get
        the icici splitter code
        Arguments:
            parser_address(str): Input address
        Returns:
            result_dict(str) : ICIC address splitted address
        Raises:
        """
        result_dict = {
            "PIN code": "",
            "House/Flat Number": "",
            "Premise/Bldg Name": "",
            "Street Number": "",
            "Locality/Area": "",
            "Landmark/Suburb": "",
            "City": "",
            "State": "",
            "Country": "",
            "ZIP Code": ""
        }

        parser_address = re.sub(r",", " ", parser_address)
        parser_address = parser_address.split(" ")
        split_dict = parse_address(parser_address)
        if "pincode" in split_dict.keys():
            result_dict["PIN code"] = split_dict["pincode"]
        if "city" in split_dict.keys():
            result_dict["City"] = split_dict["city"]
        if "state" in split_dict.keys():
            result_dict[
                "State"] = split_dict["state"]

        if "house_number" in split_dict.keys():
            if (
                    re.match(
                        "^[a-zA-Z]+.*[0-9]$", split_dict[
                            "house_number"]) is not None
                    or re.match(
                        "^.[0-9]+", split_dict[
                            "house_number"]) is not None
            ):
                result_dict[
                    "House/Flat Number"] = split_dict["house_number"]
            else:
                address_ = self.parser_address
                if result_dict["House/Flat Number"] is not None:
                    address_ = re.sub(
                        result_dict["House/Flat Number"], "", address_)
                    hno, _ = self.extract_houseno(address_)
                    result_dict[
                        "House/Flat Number"] = hno

        zipcode = re.search("^[0-9]{5}$", self.parser_address)
        if zipcode is not None:
            result_dict["ZIP Code"] = zipcode.group()
        else:
            result_dict["ZIP Code"] = None

        if "street_number" in split_dict.keys():
            if split_dict["street_number"] is not None:
                result_dict[
                    "Street Number"] = split_dict["street_number"]
            else:
                result_dict["Street Number"] = None
        else:
            result_dict["Street Number"] = None


            if "premise_name" in split_dict.keys():

                if split_dict["premise_name"] is not None:
                    result_dict[
                        "Premise/Bldg Name"] = split_dict["premise_name"]
                else:
                    result_dict["Premise/Bldg Name"] = None
            else:
                result_dict["Premise/Bldg Name"] = None

            if "locality" in split_dict.keys():
                if split_dict["locality"] is not None:
                    result_dict["Locality/Area"] = split_dict["locality"]
                else:
                    result_dict["Locality/Area"] = None
            else:
                result_dict["Locality/Area"] = None

            if "landmark" in split_dict.keys():
                if split_dict["landmark"] is not None:
                    result_dict["Landmark/Suburb"] = split_dict["landmark"]
                else:
                    result_dict["Landmark/Suburb"] = None
            else:
                result_dict["Landmark/Suburb"] = None


            for _, c in enumerate(Constant.COUNTRIES):
                parser_address = " ".join(parser_address)
                country_match = re.search(parser_address.lower(), c.lower())
                if country_match is not None:
                    result_dict["Country"] = country_match.group()
                    break
                else:
                    result_dict["Country"] = None

        return result_dict


    def cal_address_match_fuzzy_score(self)->Union[float,dict]:
        """
        This method is used to calculate
        matching score b/w parser address
        and actual address will return
        dictionary only if all the element
        is all_core_dict is an empty string
        and actual address

        Arguments:
            None
        Returns:
          result_dict(str) : ICIC address splitted address
          total(float) : Matching score of two address
        Raises:
        """

        try:
            pin_match = False
            house_no_match = False
            parser_address = self.parser_address.lower()
            real_address = Helper.address_preprocessor(
                self.addr1,
                self.addr2,
                self.addr3,
                self.addr4,
                self.city,
                self.state,
                self.country,
                self.zipcode
            )


            if (
                    self.addr1 == ""
                    and self.addr2 == ""
                    and self.addr3 == ""
                    and self.addr4 == ""
                    and self.city == ""
                    and self.state == ""
                    and self.pincode == ""
                    and self.country == ""
                    and self.zipcode == ""
                    and self.parser_address is not None
            ):
                result_dict = self.get_icici_address_splitter(
                    self.parser_address)
                return result_dict

            try:
                pin = Helper.cleantext_address(self.pincode)
                pin = pin.strip()
                paddress = Helper.cleantext_address(self.parser_address)
                if re.search(pin, paddress) is not None:
                    parser_address = re.sub(pin, "", parser_address)
                    real_address = re.sub(pin, "", real_address)
                    if len(pin) >= 5:
                        pin_match = True

                if pin_match is False and len(pin) < 6:
                    pin_five_digits = self.pincode[:5]
                    if re.search(pin_five_digits, parser_address) is not None:
                        parser_address = re.sub(
                            pin_five_digits, "", parser_address)
                        real_address = re.sub(pin_five_digits, "", real_address)
                        if len(self.pincode) >= 5:
                            pin_match = True

            except Exception as error:
                real_address = re.sub(self.pincode, "", real_address)
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace_back = traceback.TracebackException(exc_type,
                                                          exc_value, exc_tb)
                error_msg = "".join(trace_back.format_exception_only())
                self.logger.ml_logger(
                    level="ERROR",
                    ml_package="address_match",
                    message = f"{error_msg} - {trace_back}",
                    status_code=self.error_dict["ERROR_ADDRESS_MATCH"]["code"],
                    request_id=self.request_id,
                    page_id=self.page_id,
                )

                raise DocAIException(
                    action="Invalid house no",
                    message=f"{error_msg} - {trace_back}",
                    status_desc=self.error_dict["ERROR_ADDRESS_MATCH"]["desc"],
                    status_code=self.error_dict["ERROR_ADDRESS_MATCH"]["code"],
                ) from error
            hno, hno_digits = self.extract_houseno(
                Helper.cleantext_address(self.addr1))
            real_address = re.sub(hno, "", real_address)
            if hno_digits is not None:
                hno_digits = int(hno_digits)

            try:
                parser_address = Helper.cleantext_address(parser_address)
                hno_search = re.search(hno, parser_address)
                hno_pred = None
                if hno_search is not None:
                    hno_pred = hno_search.group()
                    house_no_match = True
                    if hno == str(hno_digits):
                        if hno == hno_pred:
                            house_no_match = True
                            real_address = re.sub(
                                hno_pred.lower(), "", real_address)
                            parser_address = re.sub(
                                hno_pred, "", parser_address)
                    else:
                        digit = [c for c in hno_pred if c.isdigit()]
                        digits = "".join(digit)
                        if digits == str(hno_digits):
                            house_no_match = True
                            real_address = re.sub(hno_pred, "", real_address)
                            parser_address = re.sub(
                                hno_pred, "", parser_address)
                else:
                    hno_search = re.search(str(hno_digits), parser_address)
                    if hno_search is not None:
                        hno_pred = hno_search.group()
                        house_no_match = True
                        real_address = re.sub(hno_pred, "", real_address)
                        parser_address = re.sub(hno_pred, "", parser_address)

                self.logger.ml_logger(
                    level="INFO",
                    ml_package="docai-fuzzymatch",
                    action="Fuzzy Match address",
                    status_code=200,
                    message="House No Predicted -->{} and"
                            " pincode --> {}",
                    request_id=self.request_id,
                    page_id=self.page_id
                )

            except Exception as error:
                real_address = re.sub(hno, "", real_address)
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace_back = traceback.TracebackException(exc_type,
                                                          exc_value, exc_tb)
                error_msg = "".join(trace_back.format_exception_only())
                self.logger.ml_logger(
                    level="ERROR",
                    ml_package="address_match",
                    message = f"{error_msg} - {trace_back}",
                    status_code=self.error_dict["ERROR_ADDRESS_MATCH"]["code"],
                    request_id=self.request_id,
                    page_id=self.page_id,
                )

                raise DocAIException(
                    action="Invalid house no",
                    message=f"{error_msg} - {trace_back}",
                    status_desc=self.error_dict["ERROR_ADDRESS_MATCH"]["desc"],
                    status_code=self.error_dict["ERROR_ADDRESS_MATCH"]["code"],
                ) from error

            if pin_match is False or house_no_match is False:
                if hno_digits is not None and self.pincode != "":
                    return float(0)
                if pin_match is False:
                    return float(0)
                real_address = Helper.cleantext_address(real_address)
                real_address = real_address.replace(" ","")
                paddress = parser_address
                parser_address = parser_address.replace(" ","")
                fuzz_score = fuzz.ratio(real_address, parser_address)
                return (
                    (
                        Constant.HNO_WEIGHT+Constant.PIN_WEIGHT+
                        Constant.ADDRESS_WEIGHT*fuzz_score))/100
            else:
                real_address = Helper.cleantext_address(real_address)
                real_address = real_address.replace(" ","")
                paddress = parser_address
                parser_address = parser_address.replace(" ","")
                fuzz_score = fuzz.ratio(real_address, parser_address)
                total = (
                    (Constant.HNO_WEIGHT+
                     Constant.PIN_WEIGHT+
                     Constant.ADDRESS_WEIGHT*fuzz_score))/100
                return round(float(total),2)

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(exc_type,
                                                      exc_value, exc_tb)
            error_msg = self.error_dict["ERROR_ADDRESS_MATCH"]["desc"]
            self.logger.ml_logger(
                    level="ERROR",
                    ml_package="address_match",
                    message = f"{error_msg} - {trace_back}",
                    status_code=self.error_dict["ERROR_ADDRESS_MATCH"]["code"],
                    request_id=self.request_id,
                    page_id=self.page_id,
                )

            raise DocAIException(
                action="Invalid house no",
                message=f"{error_msg} - {trace_back}",
                status_desc=self.error_dict["ERROR_ADDRESS_MATCH"]["desc"],
                status_code=self.error_dict["ERROR_ADDRESS_MATCH"]["code"],
            ) from error
            