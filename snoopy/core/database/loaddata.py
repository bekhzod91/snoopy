import os
import re
from flask import current_app as app
from snoopy.core import db
from sqlalchemy import inspect

from ..parser import YamlLoader


class PrimaryKeyNotProvide(Exception):
    pass


class ModelNotProvide(Exception):
    pass


def load_fixtures(fixtures: list[str], loader=YamlLoader):
    for fixture in fixtures:
        project_dir = app.config["PROJECT_DIR"]
        fixture_full_path = os.path.join(project_dir, "tests", fixture)

        with open(fixture_full_path) as f:
            records = loader.parse(f.read()) or []

            models = {
                re.sub(
                    r'^.*?\.(.*?)\..*\.(.*)$',
                    r'\1.\2',
                    f'{mapper.class_.__module__}.{mapper.class_.__name__}'
                ): mapper.class_
                for mapper in db.Model.registry.mappers
            }

            for record in records:
                model = record.get("model")
                model_class_ = models.get(model)

                pk = record.get("pk")
                pk_fields = inspect(model_class_).primary_key

                if not model or not model_class_:
                    raise ModelNotProvide(
                        f"Model {model} for fixtures {fixture_full_path} not found."
                    )

                if len(pk_fields) > 0 and not pk:
                    raise PrimaryKeyNotProvide(
                        f"PrimaryKey for fixtures {fixture_full_path} not provide."
                    )

                pk_field_name = pk_fields[0].name

                instance = model_class_(**record["fields"])
                setattr(instance, pk_field_name, pk)

                db.session.add(instance)
