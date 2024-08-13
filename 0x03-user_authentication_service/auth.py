#!/usr/bin/env python3
"""
hash password return salted hash
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
    - password: A string representing the password to be hashed.

    Returns:
    - A bytes object containing the hashed password.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed
