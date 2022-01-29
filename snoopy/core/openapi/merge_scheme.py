import os
from flask import current_app as app

from ..parser import YamlLoader


def replace_ref(obj: dict | list, root: dict) -> str:
    swagger_path = os.path.join(app.config["PROJECT_DIR"], "swagger")
    scheme_path = os.path.join(swagger_path, obj["$ref"])

    with open(scheme_path) as f:
        content = YamlLoader.parse(f.read())
        title = content["title"]

        if not root.get("components"):
            root["components"] = {}

        if not root["components"].get("schemas"):
            root["components"]["schemas"] = {}

        root["components"]["schemas"][title] = content

        return f"#/components/schemas/{title}"


def walk_by_tree(obj: dict | list, root: dict) -> dict | list:
    if type(obj) == dict:
        for key in list(obj.keys()):
            if key == "$ref":
                obj[key] = replace_ref(obj, root)
            else:
                obj[key] = walk_by_tree(obj[key], root)

        return obj

    if type(obj) == list:
        for idx, item in enumerate(obj):
            obj[idx] = walk_by_tree(item, root)

        return obj

    return obj


def merge_scheme(root: dict) -> dict:
    return walk_by_tree(root, root)
