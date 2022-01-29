from flask import Response


def test_ping(client):
    response: "Response" = client.get("/ping/")

    status_code = response.status_code
    data = response.json

    assert status_code == 200
    assert data["message"] == "pong"



