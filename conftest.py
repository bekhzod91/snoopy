import pytest

from snoopy.core import create_app
from snoopy.core import db
from flask_migrate import upgrade

app = create_app()


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(name="db")
def database():
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
