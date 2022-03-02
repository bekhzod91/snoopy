from http import HTTPStatus

from flask import Flask
from flask.testing import Client
from flask_sqlalchemy import SQLAlchemy

from snoopy.core import load_fixtures
from snoopy.auth.models.user import User


def test_forgot_password_flow(app: "Flask", client: "Client", db: "SQLAlchemy"):
    load_fixtures(["fixtures/auth/test_forgot_password_flow.yaml"])

    body = {
        "username": "admin@example.com"
    }

    # Request to forgot password
    with app.app_context():
        response = client.post("/api/v1/auth/forgot-password/", json=body)
        status_code = response.status_code
        assert status_code == HTTPStatus.NO_CONTENT

    # Set new password
    user = User.query.filter_by(username="admin@example.com").one()
    body = {
        "token": user.forgot_password_token,
        "new_password": "MyRandomText1234"
    }
    with app.app_context():
        response = client.post("/api/v1/auth/forgot-password/confirm/", json=body)
        status_code = response.status_code
        assert status_code == HTTPStatus.NO_CONTENT, response.json

    # Try to log in
    body = {
        "username": "admin@example.com",
        "password": "MyRandomText1234"
    }
    with app.app_context():
        response = client.post("/api/v1/auth/sign-in/", json=body)
        status_code = response.status_code
        assert status_code == HTTPStatus.CREATED
