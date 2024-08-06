#!/usr/bin/env python3
"""
create a class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for the given path.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the authorization header from the request.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user from the request.
        """
        return None
