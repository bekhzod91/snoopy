from http import HTTPStatus

import pytest
from flask import Flask
from flask.testing import Client
from flask_sqlalchemy import SQLAlchemy

from snoopy.core import load_fixtures
from snoopy.auth.models.user import User


@pytest.mark.main
def test_forgot_password_confirm(app: "Flask", client: "Client", db: "SQLAlchemy"):
    load_fixtures(["fixtures/auth/test_forgot_password_confirm.yaml"])
    body = {
        "token": "YW1peJ514UVEwOe6_-lGq2AOGqYlONOfd3MVfdXG",
        "new_password": "NewTest1234"
    }

    with app.app_context():
        response = client.post("/api/v1/auth/forgot-password/confirm/", json=body)
        status_code = response.status_code

    assert status_code == HTTPStatus.NO_CONTENT

    user = User.query.filter_by(username="admin@example.com").one()
    assert user.password_verify("NewTest1234")
    assert user.forgot_password_token is None
    assert user.forgot_password_expire is None


def test_forgot_password_confirm_with_wrong_token(
        app: "Flask", client: "Client", db: "SQLAlchemy"
):
    body = {
        "token": "69tcSlsA8GKaxWkNf_uFpcQKiJ993xghIVNwWfIB",
        "new_password": "NewTest1234"
    }

    with app.app_context():
        response = client.post("/api/v1/auth/forgot-password/confirm/", json=body)
        status_code = response.status_code
        data = response.json

    assert status_code == HTTPStatus.BAD_REQUEST
    assert data["code"] == "invalid_forgot_password_token"
    assert data["message"] == "Invalid forgot password token."


def test_forgot_password_confirm_password_is_week(
        app: "Flask", client: "Client", db: "SQLAlchemy"
):
    load_fixtures(["fixtures/auth/test_forgot_password_confirm_with_empty_password.yaml"])

    body = {
        "token": "qx8S4v-zAetcek_NlOxV_cD1FrTfZ0LGw7i88N4K",
        "new_password": "12"
    }

    with app.app_context():
        response = client.post("/api/v1/auth/forgot-password/confirm/", json=body)
        status_code = response.status_code
        data = response.json

    assert status_code == HTTPStatus.BAD_REQUEST
    assert data["code"] == "new_password_is_week"
    assert data["message"] == (
        "New password is week. "
        "Password should contain 8 characters!"
    )


def test_forgot_password_confirm_with_emtpy_data(
        app: "Flask", client: "Client", db: "SQLAlchemy"
):
    with app.app_context():
        response = client.post("/api/v1/auth/forgot-password/confirm/", json={})
        status_code = response.status_code
        data = response.json

    assert status_code == HTTPStatus.BAD_REQUEST
    assert data["code"] == "validation_error"
    assert data["message"] == "Validation error. Check your detail!"


def test_forgot_password_confirm_with_expire_token(
        app: "Flask", client: "Client", db: "SQLAlchemy"
):
    load_fixtures(["fixtures/auth/test_forgot_password_confirm_with_expire_token.yaml"])

    body = {
        "token": "GV7WsxhSV6WxGUgeKzhDslOGCuzFXgzvC56VwZmb",
        "new_password": "Test1245"
    }

    with app.app_context():
        response = client.post("/api/v1/auth/forgot-password/confirm/", json=body)
        status_code = response.status_code
        data = response.json

    assert status_code == HTTPStatus.BAD_REQUEST
    assert data["code"] == "invalid_forgot_password_token"
    assert data["message"] == "Invalid forgot password token."

    user = User.query.filter_by(username="admin@example.com").one()
    assert user.forgot_password_token is None
    assert user.forgot_password_expire is None
