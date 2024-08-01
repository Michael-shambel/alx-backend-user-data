#!/usr/bin/env python3
"""
unction called filter_datum that returns the log message obfuscated
"""
import re
from typing import List


def filter_datum(fields, redaction, message, separator):
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m:
                  f"{m.group().split('=')[0]}={redaction}", message)
