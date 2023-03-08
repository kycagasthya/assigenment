# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
""" helpers.py will contain methods that will be used by fuzzylogic.py"""

from fuzzywuzzy import fuzz
from .constant import Constant
import re


class Helper:
    @staticmethod
    def cleantext(inp_ent: str) -> str:
        """
        This methods does the reuired text cleaning
        of the input names
        Arguments:
            inp_ent (str):input name
        Returns:
            cleaned string name
        """
        inp_ent = inp_ent.lower()
        inp_ent = re.sub(r"\s+"," ",inp_ent)
        for _, word in enumerate(
            Constant.REPLACE_LIST_NAME_EXTRAS_WITH_PARANTHESIS):
            inp_ent = inp_ent.replace(word.lower(), " ")
        for _, word in enumerate(
            Constant.REPLACE_LIST_NAME_EXTRAS_NO_PARANTHESIS):
            inp_ent = inp_ent.replace(word.lower(), " ")
        inp_ent = re.sub(Constant.NAME_SUB_STRING, "", inp_ent, flags=re.I)
        inp_ent = re.sub("[!,*)@#%(&$_?.^'-:\\{}~=<>;]+", "", inp_ent)
        inp_ent = inp_ent.rstrip()
        inp_ent = inp_ent.lstrip()
        return inp_ent

    @staticmethod
    def cleantext_address(inp_ent: str) -> str:
        """
        This methods does the required text cleaning
        removing special char and some keywords in Address
        Arguments:
            inp_ent (str):input name
        Returns:
            cleaned string name
        """
        inp_ent = inp_ent.lower()
        for _, word in enumerate(Constant.REPLACE_LIST_ADDRESS):
            inp_ent = inp_ent.replace(word.lower(), " ")

        inp_ent = re.sub(r"[!,*)@#%(&$_?.^':\\{}~=<>;]+", "", inp_ent)
        inp_ent = inp_ent.strip()

        return inp_ent

    @staticmethod
    def cal_fuzz_score(str1: str, str2: str) -> float:
        """
        Method returns fuzzy score
        Args:
            str1 (str):input string1
            str2 (str):input string2
        Returns:
            score (float):Fuzzy score
        """
        score = fuzz.ratio(str1, str2)
        return round(float(score/100),2)

    @staticmethod
    def address_preprocessor(
        addr1: str = "",
        addr2: str = "",
        addr3: str = "",
        addr4: str = "",
        city:str = "",
        state:str = "",
        country:str = "",
        zipcode:str=""
    ) -> str:
        """
        This method is used for cleaning and
        preprocessing of address
        Args:
            addr1 (str) : input address1
            addr2  :input address2
            addr3 : input address3
            addr4 :input address4
        Returns:
            address(str) :cleaned address

        """
        addr1 = re.sub("~#", " ", addr1)
        addr2 = re.sub("~#", " ", addr2)
        addr3 = re.sub("~#", " ", addr3)
        addr4 = re.sub("~#", " ", addr4)

        combined_addr = "{0} {1} {2} {3} {4} {5} {6} {7}".format(
            addr1,
            addr2,
            addr3,
            addr4,
            city,
            state,
            country,
            zipcode
        )
        combined_addr = combined_addr.lower()
        combined_addr = re.sub("[!*)@#%(&$_?.^]", "", combined_addr)
        return combined_addr
