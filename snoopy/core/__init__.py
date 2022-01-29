from .application import db
from .application import create_app
from .exceptions import SnoopyException
from .database.loader import load_models
from .database.loaddata import load_fixtures

load_models()

__all__ = ["create_app", "db", "SnoopyException", "load_fixtures"]
