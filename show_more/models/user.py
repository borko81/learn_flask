from db import db
from models.enum import UserPrivilegEnum
from helpers.for_models.models_mixin import MixinModel


class UserAbstract(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    privileg = db.Column(db.Enum(UserPrivilegEnum), nullable=False, default=UserPrivilegEnum.staff)



class UserModel(UserAbstract):
    __tablename__ = 'users'


