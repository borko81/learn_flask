from datetime import datetime, timedelta
import jwt
from werkzeug.exceptions import Unauthorized, BadRequest
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPTokenAuth
from decouple import config
from db import db
from models.user import UserModel
from manager.auth_user import AuthUserToken
from manager.validate_email_exists import validate_exists_email


class UserManager:

    @staticmethod
    def register(user_data):
        user_data['password'] = generate_password_hash(user_data['password'], method="sha256")
        if validate_exists_email(user_data['email']):
            u = UserModel(**user_data)
            try:
                db.session.add(u)
                db.session.flush()
                return AuthUserToken.encode_token(u)
            except Exception as ex:
                raise BadRequest(str(ex))
        raise BadRequest("Not valid email")


    @staticmethod
    def login(data):
        check = UserModel.query.filter_by(email=data['email']).first()
        try:
            if check and check_password_hash(check.password, data['password']):
                try:
                    return AuthUserToken.encode_token(check)
                except Exception as ex:
                    raise BadRequest("Error when try to validate token")
            raise BadRequest("Invalid token")
        except Exception:
            raise BadRequest("Invalid username or password")


    @staticmethod
    def show_all_users():
        users = UserModel.query.all()
        return users

