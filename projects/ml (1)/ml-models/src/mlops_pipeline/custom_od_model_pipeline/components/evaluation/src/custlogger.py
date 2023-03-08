# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Custom logging module for mlops components"""

import logging


def set_level(level, logger, logging) -> None:
    """
    function to set level of log
    """

    level_dict = {
        "INFO": logging.INFO,
        "ERROR": logging.ERROR
    }
    if level not in level_dict:
        logger.setLevel(logging.NOTSET)
    else:
        logger.setLevel(level_dict[level])


def set_log(
        level=None, logger=None, message: str = None,
        base_log_params: dict = {}) -> None:
    """
    function to set the log
    """

    log_level_dict = {
        "INFO": logger.info,
        "ERROR": logger.error
    }

    if level not in log_level_dict:
        logger.info(message, extra=base_log_params)
    else:
        log_level_dict[level](message, extra=base_log_params)


def ml_logger(
        type_log: str = "INFO", component: str = "NOTSET1",
        message: str = "NOTSET", status_code: str = "empty",
        json_response: str = "", traceback: str = "") -> None:
    """
    This function does the logging of ML packages

    Logging Parameters
    - component: "ml-models-pan"
    - message: "connection established"
    - status_code: "code of info or error"

     level: str="NOTSET", ml_package: str=None,
     message: str=None, status_code: int=None) -> None:
    """

    base_log_params = {
        "component": component,
        "status_code": status_code,
        "json_response": json_response,
        "traceback": traceback,
    }
    # # create logger
    logger = logging.getLogger(component)
    set_level(level=type_log, logger=logger, logging=logging)
    if type_log == "ERROR":
        log_format = '{"component":"%(component)s", "message":"%(message)s",\
        "status_code":"%(status_code)s",' ' "json_response":"%(json_response)\
        s", "traceback":"%(traceback)s"}'
    else:
        if status_code == "empty":
            log_format = '{"component":"%(component)s", \
            "message":"%(message)s"}'
        else:
            log_format = '{"component":"%(component)s", \
            "message":"%(message)s","status_code":"%(status_code)s"}'
    # create formatter
    formatter = logging.Formatter(log_format)
    # add formatter to stream Handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # add stream_handler to logger
    if logger.hasHandlers():  # clear multiple log out put
        logger.handlers.clear()
    logger.addHandler(stream_handler)
    set_log(
        level=type_log, logger=logger, message=message,
        base_log_params=base_log_params)
