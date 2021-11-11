import enum

from decouple import config
from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from marshmallow import Schema, fields

app = Flask(__name__)
db_user = config('USER_NAME_FOR_DB')
db_password = config('PASSWORD_FOR_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:5432/clothes'

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db, compare_type=True)


class User(db.Model):
    """
    User model, use func.now() to get time from server ,not by client
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Text)
    create_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())

    def __repr__(self):
        return str(self.id)

    def primary_save(self):
        db.session.add(self)
        db.session.commit()


class ColorEmun(enum.Enum):
    pink = "pink"
    black = "black"
    white = "white"
    yellow = "yellow"


class SizeEnum(enum.Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"
    xl = "xl"
    xxl = "xxl"


class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(
        db.Enum(ColorEmun), default=ColorEmun.white,
        nullable=False
    )
    size = db.Column(
        db.Enum(SizeEnum),
        default=SizeEnum.s,
        nullable=False
    )
    photo = db.Column(db.String(255), nullable=False)
    create_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())

    def __repr__(self):
        return str(self.id)

    def primary_save(self):
        db.session.add(self)
        db.session.commit()


# Schema's
class BaseUserShema(Schema):
    email = fields.Email()
    full_name = fields.String()


class UserSignInSchema(BaseUserShema):
    password = fields.String()


# Resource's
class SignUp(Resource):
    def post(self):
        data = request.get_json()
        schema = UserSignInSchema()
        errors = schema.validate(data)

        if not errors:
            u = User(**data)
            u.primary_save()
        return 201, data


# Endpoint's
api.add_resource(SignUp, '/register')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
