"""
This is a he;per module for ACCORD125

Date created: 24/02/2022
Modified on: 24/02/2022
"""
import json
import re
import proto
import pandas as pd


def get_text_json(doc_element: dict, data: dict):
    """
    This function is used to get text corresponding tokens from json.
    """

    response = ""
    for segment in doc_element["textAnchor"]["textSegments"]:
        if segment in doc_element["textAnchor"]["textSegments"]:
            if "startIndex" in list(segment.keys()):
                start_index = int(segment["startIndex"])
            else:
                start_index = 0
        else:
            start_index = 0

        end_index = int(segment["endIndex"])
        response += data["text"][start_index:end_index]
    return response


def _get_text(document, element, element_type=None):
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    if element_type == "field":
        if "textAnchor" in element.keys():
            if "textSegments" in element["textAnchor"].keys():
                for segment in element["textAnchor"]["textSegments"]:
                    if "startIndex" in segment.keys():
                        start_index = segment["startIndex"]
                    else:
                        start_index = 0

                    if segment["endIndex"]:
                        end_index = segment["endIndex"]
                    else:
                        end_index = 0
                    response += document["text"][int(start_index): int(end_index)]

    else:
        for segment in element["layout"]["textAnchor"]["textSegments"]:
            if "startIndex" in segment.keys():
                start_index = segment["startIndex"]
            else:
                start_index = 0

            if segment["endIndex"]:
                end_index = segment["endIndex"]
            else:
                end_index = 0

            response += document["text"][int(start_index): int(end_index)]
    return response


def get_y_coordinates(element):
    box = element["layout"]["boundingPoly"]["vertices"]
    y1 = min(box[0]["y"], box[1]["y"], box[2]["y"], box[3]["y"])
    y2 = max(box[0]["y"], box[1]["y"], box[2]["y"], box[3]["y"])
    return y1, y2


def get_x_coordinates(element):
    box = element["layout"]["boundingPoly"]["vertices"]
    x1 = min(box[0]["x"], box[1]["x"], box[2]["x"], box[3]["x"])
    x2 = max(box[0]["x"], box[1]["x"], box[2]["x"], box[3]["x"])
    return x1, x2