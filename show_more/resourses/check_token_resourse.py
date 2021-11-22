from functools import wraps

from flask import request
from flask_restful import Resource, abort
from manager.auth_user import auth, AuthUserToken
from shemas.user_schemas import UserResponseSchema
from models.enum import UserPrivilegEnum


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = auth.current_user()
            if not user.privileg == permission:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


class CheckToken(Resource):
    @auth.login_required
    @permission_required(UserPrivilegEnum.staff)
    def get(self):
        r = request.headers['Authorization'].split()[-1]
        print(AuthUserToken.decode_token(r))
        schema = UserResponseSchema()
        return {"message": "Common testing message", "user": schema.dumps(auth.current_user())}