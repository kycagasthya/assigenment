# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
#
"""This helpers could be used for entity extraction of all parsers"""

import re
from typing import Optional
from typing import Union
from typing import List
from typing import Tuple
import string
from fuzzywuzzy import fuzz


class Utils:
    """
    used for checking alphanumeric charecter, get regular expresion results
    validate the voter id, ngram split and for fuzzy matching

    Helper class includes methods contains_letter_and_number, pass_reg,
    validate, ngrams, fuzzy.

    Attributes:
        regex: regex pattern passed from voter_parser.py,
        possible_values:fuzzy match a possible word in the input string
    """

    @staticmethod
    def clean_text(full_text: str) -> str:
        """
        This function cleans the text input by removing
        non-english characters, removes extra whitespaces

        Args:
            full_text: full text from the OCR json response.

        Returns:
            text: cleaned text
        """
        text = re.sub(rf"[^a-zA-Z0-9\s{string.punctuation}]", "", full_text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        return text

    @staticmethod
    def pass_reg(
        regex: str, full_text: str, regex_flag: Union[re.RegexFlag, int] = 0
    ) -> Optional[str]:
        """
        Find the sub string that matches the pattern

        Args:
            regex: The regex pattern to check for a match,
            full_text: string from the OCR json response,
            regex_flag: flags to be passed to regex findall method.

        Returns:
            entity: value that matches the regex pattern.
        """
        # extracting entity from string
        entity = re.findall(regex, full_text, flags=regex_flag)
        if len(entity) != 0:
            entity = entity[0].strip()
            return entity
        return None

    @staticmethod
    def ngrams(sentence: str, ngram_range: Tuple[int, int]) -> List[str]:
        """
        To get the ngrams from a sentence within a given range

        Args:
            sentence: text from the OCR json response.
            ngram_range: the range of ngrams to be extracted.

        Returns:
            ngrams_list: List of ngrams within a range from the sentence.

        """
        words = sentence.split()
        ngrams_list = []
        for i in range(ngram_range[0], ngram_range[1] + 1):
            grams = [" ".join(words[
                j : j + i]) for j in range(len(words) - i + 1)]
            ngrams_list += grams

        return ngrams_list

    def fuzzy(
        self,
        possible_values: List[str],
        full_text: str,
        ngram_range: Tuple[int, int] = (1, 1),
        threshold: int = 80,
    ) -> Optional[str]:
        """
        This function is used to get the fuzzy matched word from string

        Args:
            possible_values: words to match,
            full_text: text from the OCR json response,
            threshold: to set a confidence for fuzzy matching,
            ngram_range: the range of ngrams to be extracted.

        Returns:
            key_name: ngram that fuzzy match the given possible_values.
            value: value within possible values that fuzzy match with key_name.

        """
        final_dict = {}
        full_text = re.sub(r"\s+", " ", full_text)
        ngrams_full_text = self.ngrams(full_text, ngram_range=ngram_range)
        for value in possible_values:
            for ngram in ngrams_full_text:
                score = fuzz.ratio(value.lower(), ngram.lower())
                if score >= threshold:
                    if ngram in final_dict:
                        if score > final_dict[ngram][0]:
                            final_dict[ngram] = score, value
                    else:
                        final_dict[ngram] = score, value

        if final_dict:
            key_name = max(final_dict, key=lambda x: final_dict[x][0])
            return key_name

        return None
