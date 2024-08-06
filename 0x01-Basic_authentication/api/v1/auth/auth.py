#!/usr/bin/env python3
"""
create a class to manage the API authentication
"""
import fnmatch
from flask import request
from typing import List, TypeVar


class Auth:
    """
    a class that choose api authontication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for the given path.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path if excluded_path[-1] == '/' else excluded_path + '/'):
                return False


        normalize_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            normalize_excluded_path = excluded_path.rstrip('/')
            if normalize_path == normalize_excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the authorization header from the request.
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        else:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user from the request.
        """
        return None
