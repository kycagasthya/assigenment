import datetime
import json
import logging
import os
import uuid
import copy
import decimal

from typing import List, Dict, Tuple

import apache_beam as beam
from google.cloud import bigquery
from apache_beam.io.gcp.pubsub import PubsubMessage

from takeoff.dl.ingest.config import common
from apache_beam.transforms.display import DisplayDataItem


class AddServiceCols(beam.DoFn):
    def process(self, element, timestamp=beam.DoFn.TimestampParam):
        """
        Add service columns to the element:
        - ingest_timestamp - when message is inserted into BQ
        - ingest_timestamp - when message is inserted into BQ
        - pubsub_message_id - ID assigned by PubSub

        :param element:
        :param timestamp:
        :return:
        """
        pubsub_message_id, message_json_data = element
        message_json_data[common.PUBSUB_MESSAGE_ID_FIELD] = pubsub_message_id
        message_json_data[common.INGEST_TIMESTAMP_FIELD] = "AUTO"  # BQ sets the timestamp value automatically
        message_json_data[common.PUBLISH_TIMESTAMP_FIELD] = datetime.datetime.utcfromtimestamp(
            float(timestamp)
        ).strftime("%Y-%m-%d %H:%M:%S.%f")  # element timestamp is message publishing time
        yield message_json_data


class ValidateMessageContent(beam.DoFn):
    """
    Validate element

    :param subscription: PubSub subscription name
    :param bq_config: BQ client config dictionary
    """

    ERROR_MESSAGE = "VALIDATION ERROR: '{}', value: '{}', subscription='{}', message: {}"

    def __init__(self, subscription, bq_config):
        super().__init__()
        self.subscription = subscription
        self.bq_config = bq_config

    def process(self, element, *args, **kwargs):
        """
        Validate element:
        - check client_name is valid, if not tag output as 'invalid_client'
        - check source_name is valid, if not tag output as 'invalid_source'
        - if both are valid set default output

        :param element:
        :return:
        """
        if element[common.CLIENT_FIELD].lower() not in self.bq_config:
            logging.error(
                self.ERROR_MESSAGE.format(
                    common.INVALID_CLIENT, element[common.CLIENT_FIELD], self.subscription, element
                )
            )
            yield beam.pvalue.TaggedOutput(common.INVALID_CLIENT, (common.INVALID_CLIENT, element))

        elif (
                element[common.CLIENT_FIELD].lower() in self.bq_config
                and element[common.SOURCE_FIELD].lower()
                not in self.bq_config[element[common.CLIENT_FIELD].lower()]["sources"]
        ):
            logging.error(
                self.ERROR_MESSAGE.format(
                    common.INVALID_SOURCE, element[common.SOURCE_FIELD], self.subscription, element
                )
            )
            yield beam.pvalue.TaggedOutput(common.INVALID_SOURCE, (common.INVALID_SOURCE, element))

        else:
            yield element


def _handle_load_error(raw_message_data):
    """
    Function handles the incoming message if it is not parsed by json.loads

    :param raw_message_data: bytes or a string from Pubsub message data
    """
    if isinstance(raw_message_data, bytes):
        try:
            loaded_data = {common.WRONG_MESSAGE_FORMAT_SUBSTITUTE: raw_message_data.decode('utf-8')}
        except UnicodeDecodeError:
            loaded_data = {common.WRONG_MESSAGE_FORMAT_SUBSTITUTE: str(raw_message_data)}
    else:
        loaded_data = {common.WRONG_MESSAGE_FORMAT_SUBSTITUTE: str(raw_message_data)}
    return loaded_data


def jsonify_pubsub_message(raw_message_data, dump_it: bool = None):
    """
    Function handles the incoming Pubsub message trying to load it into Python dictionary or its string repr

    :param raw_message_data: bytes or a string from Pubsub message data
    :param bool dump_it: flag decides if the output has to be cast to string representation
    """
    try:
        loaded_data = json.loads(raw_message_data if raw_message_data else common.EMPTY_MESSAGE_SUBSTITUTE)
    except json.decoder.JSONDecodeError as jde:
        loaded_data = _handle_load_error(raw_message_data)
    except UnicodeDecodeError:
        loaded_data = _handle_load_error(raw_message_data)
    if not isinstance(loaded_data, Dict):
        loaded_data = _handle_load_error(raw_message_data)
    if dump_it:
        return json.dumps(loaded_data, ensure_ascii=False)
    else:
        return loaded_data


def _get_nested_fields_with_types(schema, result_fields, field_name=str()):
    """
    Add all the fields including the nested ones to result_fields list.
    Nested field format is field.nested_field

    :param schema: the whole table schema or the record type schema
    :param result_fields: result fields list
    :param field_name: used for nested fields name construction
    :return:
    """
    for field in schema["fields"]:
        field_full_path_name = (f"{field_name}.{field['name']}" if field_name != "" else field['name'])
        result_fields.append(field_full_path_name + f":{field['type']}:{field['mode']}")
        if field["type"] == "RECORD":
            _get_nested_fields_with_types(field, result_fields, field_name=field_full_path_name)


class CustomSchemaField(object):
    """
    Class storing essential information about the field in expected interface schema

    :param parent_full_name: full name of the parent field; needed to differentiate between 2 fields with the same name
            but separate parent field, eg:
            {
                "parent_01": {
                    "field_xyz": "value"
                },
                "parent_02": {
                    "subparent_01": {
                        "field_xyz": "value"
                    }
                }
            }
            will store field field_xyz twice:
                - first time with parent_full_name='parent_01'
                - second time with parent_full_name='parent_02.subparent_01'
    :param name: field name
    :param field_type: The type of the field. See
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.type

    : param mode: The mode of the field. See
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.mode
    """
    def __init__(self, parent_full_name, name, field_type, mode):
        self.parent_full_name = parent_full_name
        self.name = name
        self.type = field_type
        self.mode = mode

    def get_full_path_name(self):
        return (self.parent_full_name if self.parent_full_name else "") + self.name


class SchemaValidation(object):
    """
    Class performing and storing the results of a custom message validation against the interface schema
    stored in ../sources/{client_name}/sources/{json_schema_name}.json
    """
    def __init__(self):
        self.missing_mandatory_fields = list()
        self.wrong_type_columns = list()
        self.additional_fields = list()
        self.message_passes_validation = True

    @staticmethod
    def _get_children_fields(current_field_list: List, parent_field_full_path: str = None):
        """
        Function returns all children fields and all mandatory children fields of a field defined by
        path parent_field_full_path; if the parent_field_full_path is None, function returns children fields
        of a root.

        :param List current_field_list: a result of _get_nested_fields_with_types function
        :param str parent_field_full_path: full name of the parent field;
            needed to differentiate between 2 fields with the same name but separate parent field
        """
        out_all_children_list = list()
        out_mandatory_children_list = list()
        if not parent_field_full_path:
            level = 0
            parent_field_full_path = ""
        else:
            parent_field_full_path = parent_field_full_path + "."
            level = parent_field_full_path.count(".")
        for x in [x for x in current_field_list if x.startswith(parent_field_full_path)]:
            if level == x.count("."):
                x_split = x.split(":")
                field_simple_name = x_split[0].split(".")[-1]
                out_all_children_list.append(
                    CustomSchemaField(parent_field_full_path, field_simple_name, *x_split[1:3]))
                if x_split[2] == "REQUIRED":
                    out_mandatory_children_list.append(
                        CustomSchemaField(parent_field_full_path, field_simple_name, *x_split[1:3]))
        return out_all_children_list, out_mandatory_children_list

    @staticmethod
    def _make_exception_for_timestamps(input_ddi_dict: Dict, expected_field: CustomSchemaField):
        """
        Function makes an exception for TIMESTAMP fields allowing STRING values to pass
        validation in _store_wrong_type_fields

        :param Dict input_ddi_dict: result of DisplayDataItem.get_dict()
        :param CustomSchemaField expected_field: a custom representation of a field from the expected interface schema
        """
        if 'TIMESTAMP' == expected_field.type.upper() and "STRING" == input_ddi_dict['type'].upper():
            return False
        else:
            return True

    @staticmethod
    def _make_exception_for_numeric_types(input_ddi_dict: Dict, expected_field: CustomSchemaField):
        """
        Function makes an exception for numeric fields allowing INTEGER2FLOAT conversion and vice versa to pass
        validation in _store_wrong_type_fields

        :param Dict input_ddi_dict: result of DisplayDataItem.get_dict()
        :param CustomSchemaField expected_field: a custom representation of a field from the expected interface schema
        """
        if "INTEGER" == expected_field.type.upper() and \
                (input_ddi_dict['type'].upper() in ["FLOAT", "FLOAT64", "NUMERIC"]):
            if input_ddi_dict['value'].is_integer():
                return False
        if expected_field.type.upper() in ["FLOAT", "FLOAT64", "NUMERIC"] and \
                (input_ddi_dict['type'].upper() in ["INTEGER", "INT64"]):
            return False
        return True

    def _store_additional_fields(self, input_chunk: Dict, parent_field_full_path: str, all_fields: List):
        """
        Function validates if there are any fields in input_chunk dictionary that are not present in all_fields list;
        all unexpected fields are appended to self.additional_fields list

        :param Dict input_chunk: an input dictionary to validate
        :param str parent_field_full_path: the full representation of parent field, empty for root
        :param List all_fields: a list of all fields the validation expects to be present in input_chunk
        """
        for chunk_element_key, chunk_element_value in input_chunk.items():
            if chunk_element_key not in [x.name for x in all_fields]:
                self.additional_fields.append(
                    ((parent_field_full_path + ".") if parent_field_full_path else '') + chunk_element_key)

    def _store_missing_mandatory_fields(self, input_chunk: Dict, mandatory_fields: List):
        """
        Function validates if there are any fields in mandatory_fields list that are not present in input_chunk dict;
        all missing fields are appended to self.missing_mandatory_fields list

        :param Dict input_chunk: an input dictionary to validate
        :param List mandatory_fields: a list of mandatory fields the validation expects to be present in input_chunk
        """
        for mandatory_field in mandatory_fields:
            if mandatory_field.name not in input_chunk.keys():
                self.missing_mandatory_fields.append(mandatory_field.get_full_path_name())

    def _store_wrong_type_fields(self, input_chunk: Dict, parent_field_full_path: str, all_fields: List):
        """
        Function validates if there are any fields in all_fields list that are present in input_chunk dict,
        but with data type that do not match;
        all wrong type fields are appended to self.wrong_type_columns list

        :param Dict input_chunk: an input dictionary to validate
        :param str parent_field_full_path: the full representation of parent field, empty for root
        :param List all_fields: a list of all fields the validation expects to be present in input_chunk
        """
        for expected_field in all_fields:
            if expected_field.name not in input_chunk.keys():
                continue
            current_input_field = input_chunk[expected_field.name]
            if isinstance(current_input_field, Dict):
                if expected_field.type != "RECORD":
                    self.wrong_type_columns.append(expected_field.get_full_path_name())
            elif isinstance(current_input_field, List):
                if expected_field.mode != "REPEATED":
                    self.wrong_type_columns.append(expected_field.get_full_path_name())
            elif current_input_field is None:
                if expected_field.mode not in ["NULLABLE", "REPEATED"]:
                    self.wrong_type_columns.append(expected_field.get_full_path_name())
            elif expected_field.type.upper() == "NUMERIC":
                try:
                    field_converted_value = decimal.Decimal(current_input_field)
                except decimal.InvalidOperation as conversion_error:
                    self.wrong_type_columns.append(expected_field.get_full_path_name())
            else:
                ddi = DisplayDataItem(input_chunk[expected_field.name],
                                      namespace=parent_field_full_path if parent_field_full_path else "/root/",
                                      key=expected_field.name)
                ddi_dict = ddi.get_dict()
                if (ddi_dict['type'] != expected_field.type) and \
                        SchemaValidation._make_exception_for_timestamps(ddi_dict, expected_field) and \
                        SchemaValidation._make_exception_for_numeric_types(ddi_dict, expected_field):
                    self.wrong_type_columns.append(expected_field.get_full_path_name())

    def _validate_children_fields(self, current_field_list: List, input_chunk, parent_field_full_path):
        """
        Function performs validation on a chunk of a Pubsub message

        :param List current_field_list: a result of _get_nested_fields_with_types function
        :param input_chunk: a chunk of a Pubsub message; may be Dict, List or a simple field
        :param str parent_field_full_path: the full representation of parent field, empty for root
        """
        all_fields, mandatory_fields = self._get_children_fields(current_field_list, parent_field_full_path)
        if not isinstance(input_chunk, Dict):
            return
        self._store_additional_fields(input_chunk, parent_field_full_path, all_fields)
        self._store_missing_mandatory_fields(input_chunk, mandatory_fields)
        self._store_wrong_type_fields(input_chunk, parent_field_full_path, all_fields)

    def message_satisfies_schema(self, current_interface_fields: List, input_message,
                                 parent_field_full_path: str = None, current_field_name: str = None):
        """
        Function performs validation on an entire Pubsub message against the flattened expected message schema;
        calls itself recursively for each dictionary and list field

        :param List current_interface_fields: a result of _get_nested_fields_with_types function
        :param input_message: an entire Pubsub message
        :param str parent_field_full_path: the full representation of parent field, empty for root
        :param str current_field_name: the name of the field under validation, empty for root
        """
        self._validate_children_fields(current_interface_fields, input_message, parent_field_full_path)
        if isinstance(input_message, Dict):
            for msg_key, msg_value in input_message.items():
                new_parent_field_full_path = \
                    (parent_field_full_path + "." if parent_field_full_path else '') + msg_key
                if isinstance(msg_value, List):
                    for list_element in msg_value:
                        self.message_satisfies_schema(
                            current_interface_fields, list_element, new_parent_field_full_path, msg_key)
                elif isinstance(msg_value, Dict):
                    self.message_satisfies_schema(
                        current_interface_fields, msg_value, new_parent_field_full_path, msg_key)
        elif isinstance(input_message, List):
            for list_element in input_message:
                new_parent_field_full_path = parent_field_full_path
                self.message_satisfies_schema(
                    current_interface_fields, list_element, new_parent_field_full_path, current_field_name)
        else:
            pass

    def check_errors_and_log_if_present(self, input_dictionary: Dict):
        """
        Function passes the final judgement of the message validity and logs a helpful error message if needed

        :param Dict input_dictionary: validated Pubsub message
        """
        if self.missing_mandatory_fields or self.wrong_type_columns or self.additional_fields:
            self.message_passes_validation = False
            logging.error(ValidateMessageSchema.ERROR_MESSAGE.format(
                "Invalid message",
                f"missing_mandatory_fields: {self.missing_mandatory_fields} \n "
                f"wrong_type_columns: {self.wrong_type_columns} \n"
                f"additional_fields: {self.additional_fields}",
                '',
                input_dictionary
            ))


def validate_message_schema(input_dictionary: Dict, client_name: str, json_schema_name: str):
    """
    Function loads necessary interface schema from the installation package,
    creates SchemaValidation object, triggers the message validation and returns validation result

    :param Dict input_dictionary: validated Pubsub message
    :param str client_name: the name of the client that is supposed to send the Pubsub message
    :param str json_schema_name: the name of the json file with the definition of the interface schema
    """
    config_file_path = os.path.join(os.path.dirname(__file__),
                                    f'../sources/{client_name}/sources/{json_schema_name}.json')
    try:
        with open(config_file_path) as schema_file:
            current_interface_definition = json.load(schema_file)
    except Exception as E:
        logging.error(f"Did not found schema {config_file_path}")
        logging.error(E.args)
        return False
    current_interface_fields = list()
    _get_nested_fields_with_types(current_interface_definition, current_interface_fields)
    element = copy.deepcopy(input_dictionary)
    if common.INGEST_TIMESTAMP_FIELD in element.keys():
        element.pop(common.INGEST_TIMESTAMP_FIELD)
    if common.PUBLISH_TIMESTAMP_FIELD in element.keys():
        element.pop(common.PUBLISH_TIMESTAMP_FIELD)
    if common.PUBSUB_MESSAGE_ID_FIELD in element.keys():
        element.pop(common.PUBSUB_MESSAGE_ID_FIELD)
    sv = SchemaValidation()
    sv.message_satisfies_schema(current_interface_fields, element)
    sv.check_errors_and_log_if_present(input_dictionary)
    return sv.message_passes_validation


class ValidateMessageSchema(beam.DoFn):
    """
    Validate element
    :param subscription: PubSub subscription name
    """

    ERROR_MESSAGE = "SCHEMA VALIDATION ERROR: '{}', value: '{}', subscription='{}', message: {}"

    def __init__(self, subscription):
        super().__init__()
        self.subscription = subscription
        self.client_name, self.json_schema_name = self.parse_subscription_name(self.subscription)

    @staticmethod
    def find_second_last(input_text, character):
        return input_text.rfind(character, 0, input_text.rfind(character))

    @staticmethod
    def parse_subscription_name(subscription):
        """
        Functions decouples client name and interface name from subscription name
        :param subscription: PubSub subscription name
        """
        sub_split_place = ValidateMessageSchema.find_second_last(subscription, '-')
        return subscription[:sub_split_place], subscription[sub_split_place + 1:].replace('-', "_")

    def process(self, element, *args, **kwargs):
        """
        Validate element:
        - check if MANDATORY_TECHNICAL_FIELDS are present, if not tag output as 'invalid_record'
        - check if message satisfied the interface schema, if not tag output as 'invalid_message_schema'
        - if both are valid set default output

        :param element: input data of Pubsub message that has to be validated
        """
        if not set(common.MANDATORY_TECHNICAL_FIELDS).issubset(set(element.keys())):
            logging.error(
                self.ERROR_MESSAGE.format(
                    common.INVALID_RECORD, element.get(common.CLIENT_FIELD, common.UNKNOWN_STRING_VALUE),
                    self.subscription, element
                )
            )
            yield beam.pvalue.TaggedOutput(common.INVALID_RECORD, (common.INVALID_RECORD, element))
        elif not validate_message_schema(
                element, client_name=self.client_name, json_schema_name=self.json_schema_name):
            logging.error(
                self.ERROR_MESSAGE.format(
                    common.INVALID_RECORD_SCHEMA, element.get(common.CLIENT_FIELD, common.UNKNOWN_STRING_VALUE),
                    self.subscription, element
                )
            )
            yield beam.pvalue.TaggedOutput(common.INVALID_RECORD_SCHEMA, (common.INVALID_RECORD_SCHEMA, element))
        else:
            yield element


class FormatFailedBQRow(beam.DoFn):
    def process(self, element, *args, **kwargs):
        """
        Format failed BQ row, add error_type

        :param element:
        :return:
        """
        _, row = element  # extract row from failed tuple
        yield common.INSERT_FAILED, row


class FormatErrorRow(beam.DoFn):
    """
    Prepare error row data before inserting it into error table

    :param subscription: PubSub subscription name
    """

    def __init__(self, subscription):
        super().__init__()
        self.subscription = subscription

    def process(self, element, *args, **kwargs):
        """
        Prepare error row data

        :param element:
        :return:
        """
        error_type, row = element
        error_row = {
            common.PUBSUB_SUBSCRIPTION_FIELD: self.subscription,
            common.ERROR_TYPE_FIELD: error_type,
            common.MESSAGE_FIELD: json.dumps(row, ensure_ascii=False),
            common.CLIENT_FIELD: row.get(common.CLIENT_FIELD, common.UNKNOWN_STRING_VALUE),
            common.SOURCE_FIELD: row.get(common.SOURCE_FIELD, common.UNKNOWN_STRING_VALUE),
            common.EVENT_TIMESTAMP_FIELD: row.get(common.EVENT_TIMESTAMP_FIELD,
                                                  datetime.datetime.now(datetime.timezone.utc)),
            common.SCHEMA_FIELD: row.get(common.SCHEMA_FIELD, common.UNKNOWN_STRING_VALUE),
            common.INGEST_TIMESTAMP_FIELD: row[common.INGEST_TIMESTAMP_FIELD],
            common.PUBLISH_TIMESTAMP_FIELD: row[common.PUBLISH_TIMESTAMP_FIELD],
            common.PUBSUB_MESSAGE_ID_FIELD: row.get(common.PUBSUB_MESSAGE_ID_FIELD),
        }

        yield error_row


class WriteRawToGCS(beam.DoFn):
    """
    Write batch of raw messages to the backup bucket

    :param output_path:
    """
    FILE_PREFIX = "output"

    def __init__(self, output_path):
        self.output_path = output_path

    def process(self, element, window=beam.DoFn.WindowParam):
        """
        Write batch messages to Google Cloud Storage.

        :param element:
        :param window:
        :return:
        """
        window_start_dt = window.start.to_utc_datetime()
        window_end_dt = window.end.to_utc_datetime()

        ts_format = "%Y_%m_%dT%H_%M_%S"
        window_start = window_start_dt.strftime(ts_format)
        window_end = window_end_dt.strftime(ts_format)

        filename = "-".join([self.FILE_PREFIX, window_start, window_end, str(uuid.uuid1())]) + ".json"
        path = os.path.join(
            self.output_path,
            str(window_start_dt.year),
            str(window_start_dt.month),
            str(window_start_dt.day),
            filename
        )

        _, batch = element
        with beam.io.gcsio.GcsIO().open(filename=path, mode="w") as f:
            for message in batch:
                f.write(f"{message}\n".encode("utf-8"))


class GetTableSchema(beam.DoFn):
    """
    Adds BigQuery table schema to the table name
    using BigQuery API
    """

    def __init__(self, project_id):
        """
        :param project_id: Google Cloud project id
        """
        super().__init__()
        self.project_id = project_id

    def process(self, element, *args, **kwargs):
        """
        :param element: tuple of client-source string and table id,
            e.g. ('best_client.users', 'my_project.my_dataset.my_table')
        :return: tuple of client-source string and table dictionary,
            e.g. ('best_client.users', {'table_id': 'my_project.my_dataset.my_table', 'schema': ...})
        """
        client_source, table_id = element

        client = bigquery.Client(self.project_id)

        table = client.get_table(table_id)
        schema = table.to_api_repr()['schema']
        yield client_source, {'table_id': table_id, 'schema': schema}


def _fix_dict(fields: List[dict], dict_to_fix: dict):
    """
    Replaces nulls with empty list object in REPEATED fields

    :param fields: BigQuery schema fields (List[dict])
    :param dict_to_fix: dictionary to work with (dict)
    :return: fixed dictionary (dict)
    """
    for schema_field in fields:
        field_name = schema_field['name']
        if field_name not in dict_to_fix:
            continue
        if schema_field['mode'] == 'REPEATED':
            if dict_to_fix[field_name] is None:
                dict_to_fix[field_name] = []
                continue
            elif schema_field['type'] == 'RECORD':
                for sub_dict_to_fix in dict_to_fix[field_name]:
                    _fix_dict(schema_field['fields'], sub_dict_to_fix)
        elif schema_field['type'] == 'RECORD' and dict_to_fix[field_name]:
            _fix_dict(schema_field['fields'], dict_to_fix[field_name])


def fix_null_lists(element, bq_schemas):
    """
    Replaces nulls with empty list object in REPEATED fields
    of input element message

    :param element: input element message (dict)
    :param bq_schemas: dict of client-source string and table dictionary,
            e.g. {'best_client.users': {'table_id': 'my_project.my_dataset.my_table', 'schema': ...}}
    :return: fixed element dictionary (dict)
    """
    fixed_element = element.copy()
    element_client_source = f"{element[common.CLIENT_FIELD].lower()}.{element[common.SOURCE_FIELD].lower()}"
    if element_client_source in bq_schemas:
        schema = bq_schemas[element_client_source]['schema']
        logging.info(f'BQ schema: {str(schema)}')
        logging.info(f'Element to fix: {fixed_element}')
        _fix_dict(schema['fields'], fixed_element)
    return fixed_element


def pubsub_msg_to_json_str(pubsub_msg: PubsubMessage):
    """
    Extracts message body in JSON format from PubsubMessage object

    :param PubsubMessage pubsub_msg: pubsub message object
    :return str: message body in JSON format
    """
    return json.dumps(json.loads(pubsub_msg.data), ensure_ascii=False)


def pubsub_msg_to_msg_id_and_dict(pubsub_msg: PubsubMessage):
    """
    Extracts message ID and message body as dict from PubsubMessage object

    :param PubsubMessage pubsub_msg: pubsub message object
    :return Tuple[str, dict]: tuple of message ID and message body as dict
    """
    return pubsub_msg.message_id, jsonify_pubsub_message(pubsub_msg.data)
