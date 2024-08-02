#!/usr/bin/env python3
"""
unction called filter_datum that returns the log message obfuscated
"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ('email', 'password', 'ssn', 'phone', 'address')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    returns the log message obfuscated
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    sub_str = re.sub(pattern, lambda m:
                     f"{m.group().split('=')[0]}={redaction}", message)
    return sub_str


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        constructor
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format method
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    returns a logging object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to the database
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return connection
