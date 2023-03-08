# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Utility functions for creating TFRecord data sets."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import io
import tensorflow.compat.v1 as tf
from PIL import Image


def int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def bytes_list_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


def float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def read_examples_list(path):
    """Read list of training or validation examples.

    The file is assumed to contain a single example per line where the first
    token in the line is an identifier that allows us to find the image and
    annotation xml for that example.

    For example, the line:
    xyz 3
    would allow us to find files xyz.jpg and xyz.xml (the 3 would be ignored).

    Args:
      path: absolute path to examples list file.

    Returns:
      list of example identifiers (strings).
    """
    with tf.gfile.GFile(path) as fid:
        lines = fid.readlines()
    return [line.strip().split(" ")[0] for line in lines]


def recursive_parse_xml_to_dict(xml):
    """Recursively parses XML contents to python dict.

    We assume that `object` tags are the only ones that can appear
    multiple times at the same level of a tree.

    Args:
      xml: xml tree obtained by parsing XML file contents using lxml.etree

    Returns:
      Python dictionary holding XML contents.
    """
    if not xml:
        return {xml.tag: xml.text}
    result = {}
    for child in xml:
        child_result = recursive_parse_xml_to_dict(child)
        if child.tag != "object":
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}


def class_text_to_int(label_map_dict: dict, row_label: str) -> int:
    """
    parse the index of label from dict
    Parameters:
    ----------
    label_map_dict : dict
        Dictionary contains label information
    row_label: str
        Label name
    Returns
    -------
    int
        index of label in dict
    """
    return label_map_dict[row_label]


def create_tf_example(group, path: str, label_map_dict: dict):
    """Create tf_example from  image
    Parameters:
    ----------
    group : pd.Dataframe()
        The path containing the .xml files
    path: str
        path to directory which contains images and xmls
    label_map_dict: dict
        contain label information
    Returns
    -------
    tf_example tf.train.Example()
        tf example
    """
    try:
        with tf.gfile.GFile(os.path.join(path, "{}".format(group.filename)),
                            "rb") as fid:
            encoded_jpg = fid.read()
    except tf.errors.NotFoundError:
        return False
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size
    filename = group.filename.encode("utf8")
    image_format = b"jpg"
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []
    for _, row in group.object.iterrows():
        xmins.append(row["xmin"] / width)
        xmaxs.append(row["xmax"] / width)
        ymins.append(row["ymin"] / height)
        ymaxs.append(row["ymax"] / height)
        classes_text.append(row["class"].encode("utf8"))
        classes.append(class_text_to_int(label_map_dict, row["class"]))
    tf_example = tf.train.Example(features=tf.train.Features(feature={
        "image/height": int64_feature(height),
        "image/width": int64_feature(width),
        "image/filename": bytes_feature(filename),
        "image/source_id": bytes_feature(filename),
        "image/encoded": bytes_feature(encoded_jpg),
        "image/format": bytes_feature(image_format),
        "image/object/bbox/xmin": float_list_feature(xmins),
        "image/object/bbox/xmax": float_list_feature(xmaxs),
        "image/object/bbox/ymin": float_list_feature(ymins),
        "image/object/bbox/ymax": float_list_feature(ymaxs),
        "image/object/class/text": bytes_list_feature(
            classes_text),
        "image/object/class/label": int64_list_feature(classes),
    }))
    return tf_example
