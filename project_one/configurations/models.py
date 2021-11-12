from datetime import datetime, timedelta

import jwt
from decouple import config

from configurations import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return str(self.id)

    def primary_save(self):
        self.password = generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def encode_token(self):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=10),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                key=config('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as er:
            raise er

    def decode_token(self, auth_token):
        try:
            key = config('SECRET_KEY')
            payload = jwt.decode(jwt=auth_token, key=key, algorithms=['HS256'])
            return payload['sub']
        except Exception as er:
            raise er


    @classmethod
    def find_user_by_email(cls, input_email):
        return cls.query.filter_by(email=input_email).first()


class ShopModel(db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return str(self.id)


    def primary_save(self):
        db.session.add(self)
        db.session.commit()
