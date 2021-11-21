from datetime import datetime, timedelta
from decouple import config
import jwt
from werkzeug.exceptions import Unauthorized
from flask_httpauth import HTTPTokenAuth
from models.user import ComplainerModel, ApproverModel, BaseUserModel


class AuthManager:
    @staticmethod
    def encode_token(user: BaseUserModel):
        payload = {
            "usb": user.id,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "type": user.__class__.__name__
        }
        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            info = jwt.decode(jwt=token, key=config("SECRET_KEY"), algorithms=["HS256"])
            return info['sub'], info['type']
        except Exception as ex:
            raise ex


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        user_id, type_user = AuthManager.decode_token(token)
        user = type_user.query.filter_by(id=user_id).first()
    except Exception as ex:
        raise Unauthorized("Invalid token")