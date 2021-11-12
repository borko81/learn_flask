# import module who not direct access to flask
from datetime import datetime, timedelta
import enum
from functools import wraps

# Flask module and what i need
import jwt
from decouple import config
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from marshmallow import Schema, fields, ValidationError, validate
from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPTokenAuth

# Configuration
app = Flask(__name__)
db_user = config('USER_NAME_FOR_DB')
db_password = config('PASSWORD_FOR_DB')
path = config('PATH_TO_BASE')

# TODO Maybe in class method?
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:5432/{path}'

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db, compare_type=True)
auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token: str):
    """
    Verify token
    :param token:
    :return:
    """
    try:
        user_id = User.decode_token(token)
        return User.find_by_id(user_id)
    except Exception:
        abort(400)
        # return 400


# Enum's
class ColorEmun(enum.Enum):
    pink = "Pink"
    black = "Nlack"
    white = "White"
    yellow = "Yellow"

    def __str__(self):
        """
        Because need to return value not ColorEmun.key
        :return:
        """
        return self.value


class SizeEnum(enum.Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"
    xl = "xl"
    xxl = "xxl"

    def __str__(self):
        return self.value


class UserRolesEnum(enum.Enum):
    super_admin = "super admin"
    admin = "admin"
    user = "user"


class User(db.Model):
    """
    User model, use func.now() to get time from server ,not by client???
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Text)
    create_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())
    role = db.Column(
        db.Enum(UserRolesEnum),
        default=UserRolesEnum.user,
        nullable=False
    )

    def encode_token(self):
        """
        Encode token, after success login
        :return:
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=2),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                key=config('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            raise e


    @staticmethod
    def decode_token(auth_token):
        """
        Decode token
        :param auth_token:
        :return:
        """
        try:
            key = config('SECRET_KEY')
            payload = jwt.decode(jwt=auth_token, key=key,  algorithms=["HS256"])
            return payload['sub']
        except jwt.ExpiredSignatureError as ex:
            raise ex
        except jwt.InvalidTokenError as ex:
            raise ex
        except Exception as ex:
            raise ex


    @classmethod
    def find_by_email(cls, user_email):
        return cls.query.filter_by(email=user_email).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    def __repr__(self):
        return str(self.id)

    def primary_save(self):
        db.session.add(self)
        db.session.commit()


class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(
        db.Enum(ColorEmun),
        default=ColorEmun.white,
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


# Policies
policy = PasswordPolicy.from_names(
    uppercase=1,
    numbers=1
)

name_policy = PasswordPolicy.from_names(
    uppercase=1
)


def validate_password(value):
    """
    Validate if password is ok or not use policy
    :param value:
    :return:
    """
    errors = policy.test(value)
    if errors:
        raise ValidationError("Not valid password try again")


def validate_full_name(value):
    """
    Validate full name has 1 or more upper case letter
    :param value:
    :return: raise ValidationError, when not correct value (full_name)
    """
    errors = name_policy.test(value)
    if errors:
        raise ValidationError("Not correct name!")


# Schema's
class BaseUserShema(Schema):
    """
    Use this when i return data to frontend, maybe one more to show only full_name?
    """
    email = fields.Email(required=True, validate=validate.Email())
    full_name = fields.String(required=True, validate=validate.And(validate_full_name))


class UserSignInSchema(BaseUserShema):
    password = fields.String(required=True, validate=validate.And(validate_password))


class ClothesSchema(Schema):
    """
    Use to return json obj  when success hit endpoint
    """
    id = fields.Integer()
    name = fields.String()
    color = fields.String()
    size = fields.String()
    photo = fields.String()


# Resource's
class SignUp(Resource):
    def post(self):
        data = request.get_json()
        schema = UserSignInSchema()
        errors = schema.validate(data)

        if not errors:
            data['password'] = generate_password_hash(data['password'], method='sha256')
            u = User(**data)
            if not u.find_by_email(data['email']):
                u.primary_save()
                token = u.encode_token()
                return {'user_info': BaseUserShema().dump(data), 'token': token}, 201
            else:
                return {"message": "Some param is incorect, try again"}
        return errors, 400


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = auth.current_user()
            if not user.role == permission:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


class ClothesRouter(Resource):
    @auth.login_required
    def get(self):
        current_user = auth.current_user()
        clothes = Clothes.query.all()
        schema = ClothesSchema(many=True)
        return {'data': schema.dump(clothes)}, 200


class SignIn(Resource):
    def post(self):
        data = request.get_json()
        user = User.find_by_email(data['email'])
        if user and check_password_hash(user.password, data['password']):
            token = user.encode_token()
            return {'token': token}, 200
        return {'message': 'Wrong authentication'}, 401


# Endpoint's
api.add_resource(SignUp, '/register')
api.add_resource(SignIn, "/login")
api.add_resource(ClothesRouter, '/clothes')

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
