#!/usr/bin/env python3
"""
unction called filter_datum that returns the log message obfuscated
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    subs_str = re.sub(pattern, lambda m:
                      f"{m.group().split('=')[0]}={redaction}", message)
    return subs_str
