#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    handle get request to the url
    acts as the home page
    """
    return jsonify(message="Bienvenue")


@app.route('/users', methods=['POST'])
def register_user():
    """
    handle post request to the url
    it handles to regester a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "user already exists"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    handle POST request asked by the user
    the code request email and password from url and check...
    ....if the given form is valid which is present in the database...
    ....if it is valid then it will create a session id.....
    ....and return the session id to the user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    handle DELETE request asked by the user
    the code request session id from the cookie
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_by_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """
    handle GET request asked by the user
    the code request session id from the cookie
    and return  the email of the user
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_by_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
