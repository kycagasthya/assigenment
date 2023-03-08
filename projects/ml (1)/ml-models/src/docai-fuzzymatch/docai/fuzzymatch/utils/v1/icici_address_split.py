# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

from collections import deque
from fuzzywuzzy import fuzz
import re
import json
import importlib.resources


def split_address(
    address:dict,
    splitted_json:dict)->dict:
    """
    This method is used to fetch
    address details such as house_number
    ,premise name and all the keys available
    in i-core format
    Arguments:
    Args:
        address(list): splitted address
        splitted_json(dict):contai
    Returns:
        splitted_json: extracted details dictionary
    """
    length_list = [5, 24, 9, 8, 19, 15, 30]
    with importlib.resources.open_text(
        "docai.fuzzymatch.utils.v1","shorthands.json")as file:
        shorthands = json.load(file)
    if len(address) > sum(length_list):
        address = address.lower()
        for key in shorthands.keys():
            if key in address:
                address.replace(key, shorthands[key])
        address = address.upper()
    parts_list = [
        "house_number",
        "premise_name",
        "building_level",
        "street_number",
        "street_name",
        "locality",
        "landmark",
    ]
    address_splitted = [
        n for n in address.split(" ") if n.replace(" ", "") != ""]
    address_queue = deque(address_splitted)
    i = 0
    leftovers = ""
    while address_queue and i < len(length_list):
        if len(address_queue[0]) > length_list[i]:
            i = i + 1
            continue
        else:
            t_part = address_queue.popleft()
            while (
                address_queue and len(
                    t_part + " " + address_queue[0]) <= length_list[i]
            ):
                t_part = t_part + " " + address_queue.popleft()
            splitted_json.update({parts_list[i]: t_part})
            i = i + 1
    while address_queue:
        leftovers = leftovers + " " + address_queue.popleft()
    splitted_json.update({"leftovers": leftovers})
    return splitted_json


def parse_address(address_splitted:list)->dict:
    """
    Method used to split address
    Arguments:
    Args:
        address(list): splitted address

    Returns:
         address_parts: extracted details dictionary
    """
    with importlib.resources.open_text(
        "docai.fuzzymatch.utils.v1","state_cities.json")as file:
        states_cities = json.load(file)

    with importlib.resources.open_text(
        "docai.fuzzymatch.utils.v1","shorthands.json")as file:
        shorthands = json.load(file)
    address_parts = {}
    _ = shorthands
    if isinstance(address_splitted, list):
        address_splitted = [
            f for f in address_splitted if f.replace(" ", "") != ""]
        stop_words = ["s/", "w/", "d/", "c/"]
        if (
            "print" in address_splitted[0].lower()
            or "date" in address_splitted[0].lower()
        ):
            address_splitted = address_splitted[1:]
        check_in = address_splitted[0].lower().replace(" ", "")
        for words in stop_words:
            if words in check_in:
                if "," in check_in:
                    part_interest = address_splitted[0].split(",", 1)[1]
                    address_splitted[0] = part_interest
                else:
                    address_splitted = address_splitted[1:]
                break
        full_address = " ".join(address_splitted).upper().replace("INDIA", "")
        full_address = re.sub(r"[$%#@^*!%()?<>{}~|&.]", "", full_address)
    else:
        full_address = (
            re.sub(r"[$%#@^*!%()?<>{}~|&.]", "", address_splitted)
            .upper()
            .replace("INDIA", "")
        )
    pincode_e = re.search(r"\d{3}\s{0,3}\d{3}", full_address)
    if pincode_e:
        full_address = (
            full_address.replace(pincode_e.group(0), "")
            .replace("PIN", "")
            .replace("CODE", "")
        )
        pincode = pincode_e.group(0).replace(" ", "")
    else:
        pincode = None
    address_parts.update({"pincode": pincode})
    state_percentage = []
    states = states_cities.keys()
    for state in states:
        state_percentage.append(
            [state, fuzz.token_set_ratio(state, full_address)])
        if len(state.split(" ")) > 1:
            state_percentage.append(
                [
                    state.replace(" ", ""),
                    fuzz.token_set_ratio(state.replace(" ", ""), full_address),
                    state,
                ]
            )

    def return_second(elem):
        return float(elem[1])

    state_percentage = sorted(state_percentage, key=return_second, reverse=True)
    if float(state_percentage[0][1]) > 95:
        state = state_percentage[0][0]
        full_address = full_address.replace(state.upper(), "")
    else:
        state = None
    address_parts.update({"state": state})
    if state is None:
        pass
    else:
        if len(state_percentage[0]) == 3:
            cities = states_cities[state_percentage[0][2].lower()]
        else:
            cities = states_cities[state.lower()]
        city_percentage = []
        for city in cities:
            city_percentage.append(
                [city, fuzz.token_set_ratio(city, full_address)])
        city_percentage = sorted(
            city_percentage, key=return_second, reverse=True)
        if float(city_percentage[0][1]) > 95:
            city = city_percentage[0][0]
            full_address = full_address.replace(city.upper(), "")
        else:
            city = None
        address_parts.update({"city": city})
    address_parts = split_address(full_address, address_parts)
    return address_parts
