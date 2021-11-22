from functools import wraps
from flask import request
from werkzeug.exceptions import BadRequest


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                raise BadRequest(f"Invalid data [{errors}]")
            return f(*args, **kwargs)
        return decorated_function
    return decorator