#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    handle get request to the url
    """
    return jsonify(message="Bienvenue")


@app.route('/users', methods=['POST'])
def register_user():
    """
    handle post request to the url
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "user already exists"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
