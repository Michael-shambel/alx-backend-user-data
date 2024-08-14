#!/usr/bin/env python3
"""
hash password return salted hash
"""
from typing import Optional
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _generate_uuid() -> str:
    """
    Generate a unique identifier.

    Returns:
    - A string representing the unique identifier.
    """
    return str(uuid.uuid4())


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


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user in the database.
        args:
            email: email of the user
            password: password of the user
        returns:
            if it is not in db user object
            if it is in the db error
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # hashed_password = _hash_password(password)
            # user = self._db.add_user(email, hashed_password)
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials.
        args:
            email: email of the user
            password: password of the user
        returns:
            True if the password is correct, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            input_password = password.encode('utf-8')
            return bcrypt.checkpw(input_password, user.hashed_password)
        except (NoResultFound, ValueError):
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for a user.
        args:
            email: email of the user
        returns:
            session_id of the user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Get a user from a session ID.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            pass
