#!/usr/bin/env python3
"""
Basic auth
"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """
    Basic Auth class that inherits from Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> str:
        """
        extracting base64 autorization header from the type of authontication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        decoding the authorization header to the formal input
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        extract the username and password from the decoded
        autorization_header
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        user_credentials = decoded_base64_authorization_header.split(':', 1)
        return (user_credentials[0], user_credentials[1])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        check the creditial of the input values
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search(attributes={"email": user_email})
        except KeyError:
            return
        except Exception:
            return
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user


def current_user(self, request=None) -> TypeVar('User'):
    """
    overloads Auth and retrieves the User instance for a request
    """
    if request is None:
        return None
    authorization_header = self.authorization_header(request)
    if authorization_header is None:
        return None

    base64_authorization_header = (
        self.extract_base64_authorization_header(authorization_header)
        )
    if base64_authorization_header is None:
        return None

    decoded_base64_authorization_header = (
        self.decode_base64_authorization_header(base64_authorization_header)
        )
    if decoded_base64_authorization_header is None:
        return None

    user_email, user_pwd = self.extract_user_credentials(
        decoded_base64_authorization_header)
    if user_email is None or user_pwd is None:
        return None

    user = self.user_object_from_credentials(user_email, user_pwd)
    return user
