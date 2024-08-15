#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Register a user

    """
    response = requests.post("http://localhost:5000/users",
                            data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    log in with wrong password
    """
    response = requests.post("http://localhost:5000/sessions",
                            data={"email": email, "password": password})
    assert response.status_code == 401

def log_in(email: str, password: str) -> str:
    """
    test to log in
    """
    response = requests.post("http://localhost:5000/sessions",
                            data={"email": email, "password": password})
    assert response.status_code == 200
    assert "session_id" in response.cookies
    assert response.json() == {"email": f"{email}", "message": "logged in"}
    return response.cookies['session_id']

def profile_unlogged() -> None:
    """
    test the profile to unlogged
    """
    response = requests.get("http://localhost:5000/profile")
    assert response.status_code == 403

def profile_logged(session_id: str) -> None:
    """
    test the profile keep logged
    """
    response = requests.get("http://localhost:5000/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}

def log_out(session_id: str) -> None:
    """
    test the logout
    """
    response = requests.delete("http://localhost:5000/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200

def reset_password_token(email: str) -> str:
    """
    test rest_password_token
    """
    response = requests.post("http://localhost:5000/reset_password", data={"email": email})
    response.status_code == 200
    assert "reset_token" in response.json()
    return response.json()[["reset_token"]]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    """
    response = requests.put("http://localhost:5000/reset_password",
                            data={"email": email, "reset_token": reset_token, "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
