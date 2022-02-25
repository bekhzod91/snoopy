from http import HTTPStatus

from flask import Flask
from flask.testing import Client
from flask_sqlalchemy import SQLAlchemy

from snoopy.core import load_fixtures
from snoopy.auth import Session


def test_sign_out(app: "Flask", client: "Client", db: "SQLAlchemy"):
    load_fixtures(["fixtures/auth/test_sign_out.yaml"])

    token = "HgJKMo5hRkh5R-tlBqfI0yz5nbETKBrbtc67F7mB"

    headers = {
        "Authorization": f"Token {token}"
    }

    with app.app_context():
        response = client.post("/api/v1/auth/sign-out/", headers=headers)
        status_code = response.status_code

    session = Session.query.filter_by(token=token).first()

    assert status_code == 204
    assert not session


def test_sign_out_invalid_token(app: "Flask", client: "Client", db: "SQLAlchemy"):
    token = "sZvDaoQhGk6bMIht9pE02f6SUi4RtZKv-FYSpIPX"

    headers = {
        "Authorization": f"Token {token}"
    }

    with app.app_context():
        response = client.post("/api/v1/auth/sign-out/", headers=headers)
        status_code = response.status_code
        data = response.json

    assert status_code == HTTPStatus.UNAUTHORIZED
    assert data["code"] == "unauthorized"
    assert data["message"] == "Unauthorized."

