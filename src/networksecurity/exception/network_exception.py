import sys
from types import TracebackType
from typing import Optional


class NetworkSecurityException(Exception):
    """Custom exception with source file and line context."""

    def __init__(self, error_message: str, error_details: Optional[object] = None) -> None:
        super().__init__(error_message)
        self.error_message = self._build_detailed_error_message(error_message, error_details)

    @staticmethod
    def _build_detailed_error_message(error_message: str, error_details: Optional[object]) -> str:
        if error_details is None:
            return error_message

        exc_info = getattr(error_details, "exc_info", None)
        if exc_info is None:
            return error_message

        _, _, exc_tb = exc_info()
        if exc_tb is None or not isinstance(exc_tb, TracebackType):
            return error_message

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return (
            f"Error occurred in Python script: [{file_name}] "
            f"at line number: [{line_number}] with message: [{error_message}]"
        )

    def __str__(self) -> str:
        return self.error_message
