from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from managers.auth import AuthManager
from models.user import ComplainerModel
from db import db


class ComplainerManager:
    @staticmethod
    def register(complainer_data):
        complainer_data['password'] = generate_password_hash(complainer_data['password'], method='sha256')
        complainer = ComplainerModel(**complainer_data)
        try:
            db.session.add(complainer)
            db.session.flush()
            return AuthManager.encode_token(complainer)
        except Exception as ex:
            raise BadRequest(str(ex))

    @staticmethod
    def login(data):
        try:
            complainer = ComplainerModel.query.filter_by(email=data['email']).first()
            if complainer and check_password_hash(complainer.password, data['password']):
                return AuthManager.encode_token(complainer)
            raise Exception
        except Exception:
            raise BadRequest("Invalid data")