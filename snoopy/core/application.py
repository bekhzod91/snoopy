import os
import json
from http import HTTPStatus
from sqlalchemy import MetaData
from flask import Flask, Response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pydantic import ValidationError

from .exceptions import SnoopyException

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # ENVIRONMENT CONFIGURATION
    env = os.environ.get("ENV", "config.development")
    app.config.from_object(env)

    # SQLALCHEMY CONFIGURATION
    db.init_app(app)
    migrate.init_app(app, db)

    # REGISTER BLUEPRINT
    from snoopy.api import root_blueprint
    app.register_blueprint(root_blueprint)

    from snoopy.api import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from snoopy.core.openapi import openapi_blueprint
    app.register_blueprint(openapi_blueprint)

    @app.errorhandler(SnoopyException)
    def handle_snoopy_exception(e):
        response = Response()
        response.status_code = HTTPStatus.BAD_REQUEST
        response.data = json.dumps({
            "code": e.code,
            "message": e.message
        })
        response.content_type = "application/json"
        return response

    @app.errorhandler(ValidationError)
    def handle_validation_exception(e):
        response = Response()
        response.status_code = HTTPStatus.BAD_REQUEST
        response.data = json.dumps({
            "code": "validation_error",
            "message": "Validation error. Check your entry data!",
            "errors": e.errors()
        })
        response.content_type = "application/json"
        return response

    return app
