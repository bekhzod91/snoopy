import pytest
from contextlib import contextmanager
from snoopy.core import create_app
from snoopy.core import db
from flask import Flask
from flask_migrate import upgrade
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(name="app")
def flask_app():
    yield create_app()


@pytest.fixture
def client(app: "Flask"):
    with app.test_client() as client:
        yield client


@pytest.fixture(name="db")
def database(app: "Flask"):
    with app.app_context():
        # Alembic upgrade head
        db.drop_all()
        upgrade()

        db.session.begin()
        yield db
        db.session.rollback()


class AlembicVersion(db.Model):
    __tablename__ = "alembic_version"

    version_num = db.Column(db.String(32), primary_key=True)
