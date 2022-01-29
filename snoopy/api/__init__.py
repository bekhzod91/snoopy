import os

from flask.blueprints import Blueprint
from flask import jsonify, send_from_directory
from flask import current_app as app

from .auth import auth_blueprint


root_blueprint = Blueprint('root', __name__)


@root_blueprint.get("/ping/")
def ping():
    return jsonify({"message": "pong"})


@root_blueprint.get("/docs/")
def docs():
    swagger_path = os.path.join(app.config["PROJECT_DIR"], "swagger")
    return send_from_directory(swagger_path, "index.html")


@root_blueprint.get("/")
def welcome():
    return "Welcome to Snoopy!"


__all__ = [
    "root_blueprint",
    "auth_blueprint"
]

