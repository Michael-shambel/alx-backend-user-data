#!/usr/bin/env python3
"""
Basic Authentication module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import Tuple, TypeVar
import hashlib


class BasicAuth(Auth):
    """Basic Authentication class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str)\
            -> str:
        """
        Extracts authorization token from header
        Return
         - token string
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decodes a basic auth token
        Return
         - the decoded token
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            return b64decode(base64_authorization_header).\
                decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) \
            -> Tuple[str, str]:
        """returns the user email and password from the Base64
        decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        data = decoded_base64_authorization_header.split(":")
        return data[0], ":".join(data[1:])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password."""
        if user_email is None or type(user_email) is not str:
            return None

        if user_pwd is None or type(user_pwd) is not str:
            return None

        from models.user import User
        try:
            users = User.search({'email': user_email})

            if type(users) is not list or len(users) == 0:
                return None
            for user in users:
                hashed = hashlib.sha256(user_pwd.encode()).hexdigest().lower()
                if user.password == hashed:
                    return user
        except KeyError:
            pass
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User
        instance for a request:"""
        authorization = self.authorization_header(request)
        bs64token = self.\
            extract_base64_authorization_header(authorization)
        credentials = self.\
            decode_base64_authorization_header(bs64token)
        email, password = self.extract_user_credentials(credentials)
        return self.user_object_from_credentials(email, password)
