#!/usr/bin/env python3
"""
Basic auth
"""
from api.v1.auth.auth import Auth
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
