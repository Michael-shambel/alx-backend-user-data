#!/usr/bin/env python3
"""
unction called filter_datum that returns the log message obfuscated
"""
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    return re.sub(f"({'|'.join(fields)})=[^{separator}]*", lambda m:
                  f"{m.group().split('=')[0]}={redaction}", message)
