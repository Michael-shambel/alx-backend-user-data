#!/usr/bin/env python3
"""
Route module for session authentication
"""
from flask import Flask, Blueprint, request, jsonify
from api.v1.app import auth
from models.user import User

session_auth_views = Blueprint('session_auth', __name__)


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

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(key=session_id, value=session_id, path='/')

    return response


@session_auth_views.route('/auth_session/logout/',
                          methods=['DELETE'], strict_slashes=False)
def logout():
    """
    DELETE /api/v1/auth_session/logout:
        - Logout the current user
    """
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({})
