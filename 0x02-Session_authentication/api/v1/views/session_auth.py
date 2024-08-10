#!/usr/bin/env python3
"""
Route module for session authentication
"""
from api.v1.app import auth
from os import getenv
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, request


@session_auth_views.route('/auth_session/login/',
                          methods=['POST'], strict_slashes=False)
def login():
    """
    POST /api/v1/auth_session/login:
        - email: str
        - password: str
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            user_id = user.id
            session_id = auth.create_session(user_id)
            response = jsonify(u.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
        else:
            return jsonify(error="wrong password"), 401
    return jsonify(error="no user found for this email"), 404
