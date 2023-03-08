# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Testing Fuzzy Name match """

import unittest
from docai.fuzzymatch.utils.v1 import name_match
from docai.fuzzymatch.utils.v1 import address_match
from docai.fuzzymatch.utils.v1 import date_match
from docai.fuzzymatch.utils.v1.icici_address_split import parse_address

class TestFuzzyNameMatch(unittest.TestCase):
    """Used for name matching cases"""

    def __init__(self, *args, **kwargs) -> None:
        """initiating  VarPath class methods"""
        super().__init__(*args, **kwargs)
        self.obj = name_match.FuzzyNameMatch()

    def name_match_general_case(self,
                                str1,
                                str2,
                                actual_match_type,
                                score:float=1.0
                               ) -> None:
        """general function for test cases"""
        result = {
            "real_name": str1.lower(),
            "pred_name": str2.lower(),
            "matchingScore": score,
            "matchingType": actual_match_type,
        }
        result_map = self.obj.fuzzy_name_match(str1, str2)
        result["real_name"] = result["real_name"].lower()
        result["pred_name"] = result["pred_name"].lower()
        result_map["real_name"] = result_map["real_name"].lower()
        result_map["pred_name"] = result_map["pred_name"].lower()

        self.assertEqual(result_map, result)


    def test_case_one(self):
        str1 = "Mohit Ranjan"
        str2 = "Ranjan Mohit"
        actual_match_type = "NAME_MATCHING_SEQUENCE"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type)

    def test_case_two(self):
        str1 = "rajendra kumar saxena"
        str2 = "rajendra kumar saxena"
        actual_match_type = "EXACT_MATCH_MULTIPLE_WORD_NAME"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type)

    def test_case_three(self):
        str1 = "Mohit Ramesh Kapoor Singh"
        str2 = "S Mohit R K"
        actual_match_type = "COMBINATION_OF_RULE3_RULE4_RULE5"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type)

    def test_case_four(self):
        str1 = "Mohit Kapoor"
        str2 = "Mohit Ramesh Kapoor"
        actual_match_type = "PARTIAL_NAME_MATCH"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type)

    def test_case_five(self):
        str1 = "Mohit R Singh"
        str2 = "Mohit Ramesh Kapoor Singh"
        actual_match_type = "NO_VALID_RULE_MATCHED"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=0.68
                                    )


    def test_case_seven(self):
        result = self.obj.clean_output("mr. ram kumar ")
        self.assertEqual(result, "ram kumar")

    def test_case_eight(self):
        str1 = "Mohit Singh d"
        str2 = "d Mohit Singh"
        actual_match_type = "NAME_MATCHING_SEQUENCE"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=1.0
                                    )
    def test_case_nine(self):
        str1 = "Mohit Ramesh Kapoor Singh"
        str2 = "S Mohit R K"
        actual_match_type = "COMBINATION_OF_RULE3_RULE4_RULE5"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=1.0
                                    )
    def test_case_ten(self):
        str1 = "Mohit"
        str2 = "Mohit"
        actual_match_type = "EXACT_MATCH_SINGLE_WORD_NAME"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=1.0
                                    )

    def test_case_eleven(self):
        str1 = "Mohit K"
        str2 = "Mohit Kapoor"
        actual_match_type = "PARTIAL_NAME_MATCH_ABBREVIATION"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=1.0
                                    )
    def test_case_twelve(self):
        str1 = "mohit ramesh singh kapoor"
        str2 = "mohit rajesh singh kapoor"
        actual_match_type = "PARTIAL_NAME_MATCH"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=1.0
                                    )
    def test_case_thirteen(self):
        obj = self.obj
        result = obj.clean_output("mohit-")
        self.assertEqual(result, "mohit")

    def test_case_fourteen(self):
        str1 = "ab"
        str2 = "ac"
        actual_match_type = "NO_VALID_RULE_MATCHED"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=0.5
                                    )


    def test_case_fifteen(self):
        str1 = "Mohit R Ku S"
        str2 = "Mohit Ramesh Kapoor Singh"
        actual_match_type = "NO_VALID_RULE_MATCHED"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=0.59
                                    )
    def test_case_sixteen(self):
        str1 = "kavya balehole krishnamurtiy"
        str2 = "kavya b k"
        actual_match_type = "COMBINATION_OF_RULE3_RULE4_RULE5"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=1.0
                                    )
    def test_case_eighteen(self):
        str1 = "Vijaykant v mudaliyar"
        str2 = "Vijaykant vinoba mudaliyar"
        actual_match_type = "PARTIAL_NAME_MATCH"
        self.name_match_general_case(str1=str1,
                                     str2=str2,
                                     actual_match_type=actual_match_type,
                                     score=1.0
                                    )

class TestFuzzyDateMatch(unittest.TestCase):
    """Used for date match"""

    def __init__(self, *args, **kwargs) -> None:
        """initialised variables"""
        super().__init__(*args, **kwargs)
        self.real_date = "05/01/1992"
        self.pred_date="05/01/1992"

    def test_case_one(self):
        """testing date_match"""
        obj_date = date_match.Datevalidation(
            real_date=self.real_date,
            pred_date=self.pred_date
        )
        res=obj_date.date_validation()
        self.assertEqual(res, 1)

class TestAddressMatch(unittest.TestCase):
    """used for address match"""

    def __init__(self, *args, **kwargs) -> None:
        """initialised variables"""
        super().__init__(*args, **kwargs)

    def test_case_one(self):
        """"""
        parser_address = "A707 aparna apartments near mall\
        road shimla himachal pradesh india 313011 "
        address_dict = {"addr1": "A707",
                "addr2" : "aparna apartments",
                "addr3" : "near mall road",
                "addr4" : "",
                "city" :  "shimla",
                "state" :  "himachal pradesh",
                "country" :"india",
                "pincode" : "313011",
                "zipcode" : ""
                }
        obj_address=address_match.AddressMatch(page_id=1,
                                request_id ="1",
                                all_core_dict = address_dict,
                                parser_address= parser_address)
        result=obj_address.cal_address_match_fuzzy_score()
        self.assertNotEqual(result, 0.0)

    def test_case_two(self):
        """"""
        parser_address = "asas asasasas udaipur 313001"
        address_dict = {"addr1": "",
                "addr2" : "",
                "addr3" : "",
                "addr4" : "",
                "city" :  "",
                "state" :  "",
                "country" :"",
                "pincode" : "",
                "zipcode" : ""
                }
        obj_address=address_match.AddressMatch(page_id=1,
                                request_id ="1",
                                all_core_dict = address_dict,
                                parser_address= parser_address)
        result=obj_address.cal_address_match_fuzzy_score()
        self.assertNotEqual(result, 0)

    def test_case_three(self):
        """"""
        split_address = "f-245 chakauti sitamarhi udaipur 313001"
        ls = parse_address(split_address)
        self.assertNotEqual(type(ls), list)

    def test_case_four(self):
        """"""
        parser_address = ""
        address_dict = {"addr1": "abc",
                "addr2" : "",
                "addr3" : "",
                "addr4" : "",
                "city" :  "",
                "state" :  "",
                "country" :"",
                "pincode" : "",
                "zipcode" : ""
                }
        obj_address=address_match.AddressMatch(page_id=1,
                                request_id ="1",
                                all_core_dict = address_dict,
                                parser_address= parser_address)
        result=obj_address.cal_address_match_fuzzy_score()
        self.assertEqual(result, 0.0)
        