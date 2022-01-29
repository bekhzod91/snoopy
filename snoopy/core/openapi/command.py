import os
from flask.blueprints import Blueprint
from flask import current_app as app


from ..parser import YamlLoader, JsonLoader

from .merge_scheme import merge_scheme


openapi_blueprint = Blueprint("openapi", __name__)


@openapi_blueprint.cli.command("make-swagger")
def make_swagger():
    """Generate swagger json"""
    input_ = os.path.join(app.config["PROJECT_DIR"], "swagger", "swagger.yaml")
    output_ = os.path.join(app.config["PROJECT_DIR"], "swagger.json")

    with open(input_) as f1:
        content = YamlLoader.parse(f1.read())
        with open(output_, "wb") as f2:
            data = merge_scheme(content)
            f2.write(JsonLoader.dumps(data))
