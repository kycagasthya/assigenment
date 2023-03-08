# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Constants that are used in fuzzy name and address logic files"""


class RuleConstants:
    RULE0 = "NO_VALID_RULE_MATCHED"
    RULE1 = "EXACT_MATCH_MULTIPLE_WORD_NAME"
    RULE2 = "EXACT_MATCH_SINGLE_WORD_NAME"
    RULE3 = "NAME_MATCHING_SEQUENCE"
    RULE4 = "PARTIAL_NAME_MATCH"
    RULE5 = "PARTIAL_NAME_MATCH_ABBREVIATION"
    RULE6 = "COMBINATION_OF_RULE3_RULE4_RULE5"
