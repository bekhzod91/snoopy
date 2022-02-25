import re
from http import HTTPStatus

import pytest
from bs4 import BeautifulSoup
from flask import Flask
from flask.testing import Client
from flask_sqlalchemy import SQLAlchemy

from snoopy.core import load_fixtures
from snoopy.core import mail
from snoopy.auth.models.user import User


@pytest.mark.main
def test_forgot_password(app: "Flask", client: "Client", db: "SQLAlchemy"):
    load_fixtures(["fixtures/auth/test_forgot_password.yaml"])

    with mail.record_messages() as outbox:
        recipient = "admin@example.com"
        body = {
            "username": recipient
        }

        with app.app_context():
            response = client.post("/api/v1/auth/forgot-password/", json=body)
            status_code = response.status_code

        assert status_code == HTTPStatus.NO_CONTENT

        # Check email
        assert len(outbox) == 1
        assert outbox[0].recipients[0] == "admin@example.com"
        assert outbox[0].subject == "Forgot your password?"
        assert outbox[0].html

        # Parse token form email body
        soup = BeautifulSoup(outbox[0].html, "html.parser")
        link = soup.select_one("#button")
        token = re.findall("https://.*/forgot-password/(.*)/", link["href"])[0]

        user = User.query.filter_by(username="admin@example.com").one()
        assert user.forgot_password_token == token


def test_forgot_password_email_non_exists(app: "Flask", client: "Client", db: "SQLAlchemy"):
    with mail.record_messages() as outbox:
        body = {
            "username": "nonexists@email.com"
        }

        with app.app_context():
            response = client.post("/api/v1/auth/forgot-password/", json=body)
            status_code = response.status_code

        assert status_code == HTTPStatus.NO_CONTENT
        assert len(outbox) == 0


def test_forgot_password_invalid_email(app: "Flask", client: "Client", db: "SQLAlchemy"):
    body = {
        "username": "admin"
    }

    with app.app_context():
        response = client.post("/api/v1/auth/forgot-password/", json=body)
        status_code = response.status_code
        data = response.json

    assert status_code == HTTPStatus.BAD_REQUEST
    assert data["code"] == "invalid_email_address"
    assert data["message"] == "Invalid email address. Check your detail!"
