from functools import wraps
from flask import request
from werkzeug.exceptions import BadRequest, Forbidden


def validate_schema(schama_name):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            schema = schama_name()
            errors = schema.validate(request.get_json())
            if errors:
                raise BadRequest(f"Invalid fields {errors}")
            return f(*args, **kwargs)
        return decorated_func
    return decorator