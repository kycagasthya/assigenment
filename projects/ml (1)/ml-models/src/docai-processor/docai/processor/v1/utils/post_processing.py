# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
#
""" generic post processing script for all parsers"""

from typing import List, Dict
import re
from docai.processor.v1.utils import postprocessing_helper
from docai.processor.v1.utils import constant


class PostProcessing(postprocessing_helper.Utils):
    """
    class PostProcessing for post processing of entities from all parsers

    Args:
        shelpers.Utils: support function for post processing
    """

    def post_process_entities(
        self, doc_type: str, cde_response: List[Dict]
    ) -> List[Dict]:
        """
        post process all the entities extracted
        Args:
            doc_type: document type
            cde_response: output from cde parser

        Returns:
            cde_response: post processed output
        """
        if doc_type == "voter_card":
            cde_response = self.voter_post_process(cde_response)

        if doc_type == "driving_license":
            cde_response = self.dl_post_process(cde_response)

        if doc_type == "aadhaar_card":
            cde_response = self.aadhaar_post_process(cde_response)

        if doc_type == "passport":
            cde_response = self.passport_post_process(cde_response)

        for i, entity in enumerate(cde_response):
            key = entity["key"]
            value = entity["value"]
            cde_response[i]["value"] = self.post_process(key, value)

        return cde_response

    def post_process(self, key: str, value: str) -> str:
        """
        cleaning the entity values using regex and
        fuzzy matching to post process the entities.

        Args:
            key: the entity name
            value: the value extracted for the key

        Returns:
            value: postprocessed entity value
        """

        value = self.clean_text(value)

        if key in constant.Constant.regex:
            regex = constant.Constant.regex[key]
            match = self.pass_reg(regex, value, regex_flag=re.I)
            if match:
                value = match

        return value

    def voter_post_process(self, cde_response: List[Dict]) -> List[Dict]:
        """
        voter_card specific post processing

        Args:
            cde_response: output from cde parser

        Returns:
            cde_response: parser specific post processed output

        Raises:
        """

        for i, entity in enumerate(cde_response):
            key = entity["key"]
            value = entity["value"]
            if key == "address":
                possible_values = constant.Constant.address_keywords
                key_name = self.fuzzy(possible_values,
                                      value,
                                      ngram_range=(1, 2))
                if key_name:
                    regex = regex = r"(?:%s)\s?\.?:?:?\.?\s?(.*)" % key_name
                    match = self.pass_reg(regex, value, regex_flag=re.S)
                    if match:
                        cde_response[i]["value"] = match

            if key == "relation_name":
                possible_values = constant.Constant.relation_name_keywords
                key_name = self.fuzzy(possible_values,
                                      value,
                                      ngram_range=(1, 3))
                if key_name:
                    regex = fr"(?:{key_name})\s?\.?:?:?\.?\s?(\D.+)"
                    match = self.pass_reg(regex,
                                          value,
                                          regex_flag=re.S | re.I)
                    if match:
                        cde_response[i]["value"] = match

        return cde_response

    def dl_post_process(self, cde_response: List[Dict]) -> List[Dict]:
        """
        driving_license specific post processing

        Args:
            cde_response: output from cde parser

        Returns:
            cde_response: parser specific post processed output
        """

        for i, entity in enumerate(cde_response):
            key = entity["key"]
            value = entity["value"]
            if key == "address":
                possible_values = constant.Constant.dl_address_keywords
                for address_key in possible_values:
                    value = value.replace(address_key, "")
                cde_response[i]["value"] = value.strip()
        return cde_response

    def aadhaar_post_process(self,
                             cde_response: List[Dict]) -> List[Dict]:
        """
        aadhaar_card specific post processing

        Args:
            cde_response: output from cde parser

        Returns:
            cde_response: parser specific post processed output
        """
        temp_list = []

        for _, entity in enumerate(cde_response):
            key = entity["key"]
            value = entity["value"]
            confidence = entity["confidence"]
            if key == "aadhaar_no":
                temp_dict = {}
                temp_dict["key"] = key
                temp_dict["value"] = value
                temp_dict["confidence"] = confidence
                temp_list.append(temp_dict)
        if len(temp_list) != 0:
            sorted_list = []
            for _, entity in enumerate(temp_list):
                key = entity["key"]
                value = entity["value"]
                confidence = entity["confidence"]
                if len(sorted_list) == 0:
                    temp_dict = {}
                    temp_dict["key"] = key
                    temp_dict["value"] = value
                    temp_dict["confidence"] = confidence
                    sorted_list.append(temp_dict)
                elif len(sorted_list) != 0:
                    temp_dict = {}
                    temp_dict["key"] = key
                    temp_dict["value"] = value
                    temp_dict["confidence"] = confidence
                    previoust_confidence = sorted_list[0]["confidence"]
                    if previoust_confidence <= confidence:
                        sorted_list[0] = temp_dict

            if len(sorted_list) != 0:
                updated_list = [
                    x for x in cde_response if not "aadhaar_no" in (x.values())
                ]
                updated_list.append(sorted_list[0])
                updated_list = sorted(updated_list, key=lambda i: i["key"])
                return updated_list

        return cde_response

    def passport_post_process(self, cde_response: List[Dict]) -> List[Dict]:
        """
        passport specific post processing

        Args:
            cde_response: output from cde parser
        Returns:
            cde_response: parser specific post processed output
        """

        passport_dict = {}
        for i, entity in enumerate(cde_response):
            key = entity["key"]
            passport_dict[key] = i

        name_list = []
        if "name" in passport_dict:
            i = passport_dict["name"]
            value = cde_response[i]["value"]
            confidence = cde_response[i]["confidence"]
            name_list.append((value, confidence))
        if "surname" in passport_dict:
            i = passport_dict["surname"]
            value = cde_response[i]["value"]
            confidence = cde_response[i]["confidence"]
            name_list.append((value, confidence))

        if name_list and "name" in passport_dict:
            i = passport_dict["name"]
            cde_response[i]["value"] = " ".join([i for i, j in name_list])
            cde_response[i]["confidence"] = sum(
                [j for i, j in name_list]) / len(
                name_list
            )

        address_list = []
        if "address_line_1" in passport_dict:
            i = passport_dict["address_line_1"]
            value = cde_response[i]["value"]
            confidence = cde_response[i]["confidence"]
            address_list.append((value, confidence))
        if "address_line_2" in passport_dict:
            i = passport_dict["address_line_2"]
            value = cde_response[i]["value"]
            confidence = cde_response[i]["confidence"]
            address_list.append((value, confidence))
        if "address_line_3" in passport_dict:
            i = passport_dict["address_line_3"]
            value = cde_response[i]["value"]
            confidence = cde_response[i]["confidence"]
            address_list.append((value, confidence))

        del_list = [
            "surname",
            "address_line_1",
            "address_line_2",
            "address_line_3",
            "address",
        ]
        del_i = []
        for key in del_list:
            if key in passport_dict:
                del_i.append(passport_dict[key])
        for i in sorted(del_i, reverse=True):
            del cde_response[i]

        if address_list:
            address_dict = {}
            address_dict["key"] = "address"
            address_dict["value"] = " ".join([i for i, j in address_list])
            address_dict["confidence"] = sum(
                [j for i, j in address_list]) / len(
                address_list
            )

            cde_response.append(address_dict)

        return cde_response
