# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

""" date match to validate dates"""
from datetime import datetime
from .constant import Constant
from qdocai.logger import QDocLogger
from qdocai.utils import DocAIBase
from docai.fuzzymatch.utils.v1 import error_code
import traceback
import sys


class Datevalidation(DocAIBase):
    def __init__(
        self,
        request_id: str = "",
        page_id: int = 1,
        real_date: str = "",
        pred_date: str = "",
    )->None:
        self.real_date = real_date
        self.pred_date = pred_date
        self.logger = QDocLogger()
        self.error_dict = error_code.Errors().error_codes
        super().__init__(request_id, page_id)

    def date_validation(self)->float:
        """
        This method compares real date and
        pred date and return the matching
        output
        Arguments:
            None
        Returns:
            float(1) or float(0)
        """
        try:
            fmt = Constant.DATE_FMT
            if "-" in self.real_date and "-" in self.pred_date:
                date1 = datetime.strptime(
                    self.real_date, "%d-%m-%Y").strftime(fmt)
                date2 = datetime.strptime(
                    self.pred_date, "%d-%m-%Y").strftime(fmt)
            elif "-" in self.real_date:
                date1 = datetime.strptime(
                    self.real_date, "%d-%m-%Y").strftime(fmt)
                date2 = datetime.strptime(
                    self.pred_date, "%d/%m/%Y").strftime(fmt)
            elif "-" in self.pred_date:
                date1 = datetime.strptime(
                    self.real_date, "%d/%m/%Y").strftime(fmt)
                date2 = datetime.strptime(
                    self.pred_date, "%d-%m-%Y").strftime(fmt)
            else:
                date1 = datetime.strptime(self.real_date, fmt)
                date2 = datetime.strptime(self.pred_date, fmt)
            self.logger.ml_logger(
                level="INFO",
                ml_package="docai-fuzzymatch",
                action="Date Validation",
                status_code=200,
                message="Validating  Date 1 -->{} and"
                " Date 2 --> {}",
                request_id=self.request_id,
                page_id=self.page_id,
            )
            if bool(date1==date2):
                return float(1)

            return float(0)

        except ValueError:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict[
                    "ERROR_DATE_FORMAT"]["text_desc"]
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-fuzzymatch",
                action="Invalid_Date_Format",
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict["ERROR_DATE_FORMAT"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            return float(0)
