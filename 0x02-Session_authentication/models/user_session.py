#!/usr/bin/env python3
"""
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class to store session data in a file-based database
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    def to_json(self):
        """Convert instance to JSON."""
        return json.dumps({
            'user_id': self.user_id,
            'session_id': self.session_id,
        })

    @classmethod
    def from_json(cls, json_str):
        """Create an instance from JSON."""
        data = json.loads(json_str)
        return cls(user_id=data['user_id'], session_id=data['session_id'])
