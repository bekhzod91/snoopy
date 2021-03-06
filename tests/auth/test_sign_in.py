from http import HTTPStatus

from flask import Flask
from flask.testing import Client
from flask_sqlalchemy import SQLAlchemy

from snoopy.core import load_fixtures
from snoopy.auth import Session


def test_sign_in(app: "Flask", client: "Client", db: "SQLAlchemy"):
    load_fixtures(["fixtures/auth/test_sign_in.yaml"])

    body = {
        "username": "root",
        "password": "Test1234"
    }

    with app.app_context():
        response = client.post("/api/v1/auth/sign-in/", json=body)
        status_code = response.status_code
        data = response.json

    assert status_code == HTTPStatus.CREATED

    session = Session.query.filter_by(token=data["token"]).one()

    assert session.token == data["token"]
    assert session.user.username == "root"
    assert session.device == "werkzeug/2.0.2"
    assert session.ip_address == "127.0.0.1"
    assert session.created_at
    assert session.last_activity


def test_sign_in_strip_password(app: "Flask", client: "Client", db: "SQLAlchemy"):
    load_fixtures(["fixtures/auth/test_sign_in_strip_password.yaml"])

    body = {
        "username": "root",
        "password": "    Test1234      "
    }

    with app.app_context():
        response = client.post("/api/v1/auth/sign-in/", json=body)
        status_code = response.status_code

    assert status_code == HTTPStatus.CREATED


def test_sign_in_invalid_credential(app: "Flask", client: "Client", db: "SQLAlchemy"):
    load_fixtures(["fixtures/auth/test_sign_in_invalid_credential.yaml"])

    body = {
        "username": "root",
        "password": "test1234"
    }

    with app.app_context():
        response = client.post("/api/v1/auth/sign-in/", json=body)
        status_code = response.status_code
        data = response.json

    assert status_code == HTTPStatus.BAD_REQUEST
    assert data["code"] == "invalid_credential"
    assert data["message"] == "Invalid credential. Check your username and password!"
