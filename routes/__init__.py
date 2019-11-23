from flask import Blueprint
from flask_jsonschema import JsonSchema, ValidationError

routes = Blueprint('routes', __name__)

@routes.errorhandler(ValidationError)
def onValidationError(e):
    return "There was a validation error: " + str(e)

from .users import *