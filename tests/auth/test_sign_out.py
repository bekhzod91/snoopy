from flask.testing import Client
from flask_sqlalchemy import SQLAlchemy
from snoopy.core import load_fixtures
from snoopy.auth import Session


def test_sign_out(client: "Client", db: "SQLAlchemy"):
    load_fixtures(["fixtures/auth/test_sign_out.yaml"])

    token = "HgJKMo5hRkh5R-tlBqfI0yz5nbETKBrbtc67F7mB"

    headers = {
        "Authorization": f"Token {token}"
    }

    response = client.post("/api/v1/auth/sign-out/", headers=headers)
    status_code = response.status_code

    session = Session.query.filter_by(token=token).first()

    print(response.data)
    assert status_code == 204
    assert not session

