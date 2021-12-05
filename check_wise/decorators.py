from flask import request, abort
from werkzeug.exceptions import BadRequest


def validate_schema(schema_name):
    def decorator(f):
        def docorated_func(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                raise BadRequest(f"Invalid fields {errors}")
            return f(*args, **kwargs)

        return docorated_func

    return decorator