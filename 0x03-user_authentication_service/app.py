#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    handle get request to the url
    """
    return jsonify(message="Bienvenue")
