from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from flask_restful import abort
from werkzeug.exceptions import Unauthorized

from models.user import UserModel

auth = HTTPTokenAuth(scheme="Bearer")


class AuthUserToken:
    @staticmethod
    def encode_token(user: UserModel):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(hours=1), "type": str(user.privileg)}
        return jwt.encode(payload, key=config('SECRET_KEY'), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            info = jwt.decode(jwt=token, key=config('SECRET_KEY'), algorithms=["HS256"])
            return info['sub'], str(info['type'])
        except Exception as ex:
            raise ex


@auth.verify_token
def validate_token(token):
    try:
        user_id, type_user = AuthUserToken.decode_token(token)
        return UserModel.query.filter_by(id=user_id).first()
    except Exception as ex:
        abort(400)
