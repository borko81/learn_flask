import enum, jwt
from decouple import config
from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from sqlalchemy import func
from marshmallow import Schema, fields, validate, ValidationError
from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
db = SQLAlchemy(app)
db_user = config('USER_NAME_FOR_DB')
db_password = config('PASSWORD_FOR_DB')
path = config('PATH_TO_BASE')

# TODO Maybe in class method?
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:5432/{path}'

api = Api(app)
migrate = Migrate(app, db)
auth = HTTPTokenAuth(scheme='Bearer')

policy = PasswordPolicy.from_names(
    uppercase=1,
)


def validate_password(value):
    errors = policy.test(value)
    if errors:
        raise ValidationError(f"Not a valid password")


@auth.verify_token
def verify_token(token):
    try:
        user_id = User.decode_token(token)
        return User.query.filter_by(id=user_id).first()
    except:
        abort(400)


class ColorEnum(enum.Enum):
    pink = 'pink'
    black = 'black'
    green = 'green'
    white = 'white'
    yellow = 'yellow'


class SizeEnum(enum.Enum):
    xs = 'xs'
    s = 's'
    m = 'm'
    l = 'l'
    xl = 'xl'
    xxl = 'xxl'


class UserRolesEnum(enum.Enum):
    super_admin = 'super admin'
    admin = 'admin'
    user = 'user'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Text)
    role = db.Column(
        db.Enum(UserRolesEnum),
        default=UserRolesEnum.user,
        nullable=False
    )
    create_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())

    def encode_token(self):
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
        try:
            key = config('SECRET_KEY')
            payload = jwt.decode(
                jwt=auth_token,
                key=key,
                algorithms=['HS256']
            )
            return payload['sub']
        except jwt.ExpiredSignatureError as ex:
            raise ex
        except jwt.InvalidTokenError as ex:
            raise ex
        except Exception as ex:
            raise ex


class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(
        db.Enum(ColorEnum),
        default=ColorEnum.white,
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


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    full_name = fields.String(required=True, validate=validate.Length(min=2))


class UserSignInSchema(BaseUserSchema):
    password = fields.String(required=True, validate=validate.And(validate.Length(min=8, max=20), validate_password))


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        schema = UserSignInSchema()
        errors = schema.validate(data)
        if not errors:
            data['password'] = generate_password_hash(data['password'], method='sha256')
            user = User(**data)
            db.session.add(User(**data))
            db.session.commit()
            token = user.encode_token()
            return {'token': token}
        return {'error': errors},  400


class SignIn(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()
        if user and check_password_hash(user.password, data["password"]):
            token = user.encode_token()
            return {"token": token}, 200
        return {"messsage": "Wrong email or passwword"}, 400


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
    @permission_required(UserRolesEnum.user)
    def get(self):
        current_user = auth.current_user()
        clothes = Clothes.query.all()
        return {'data': 'clothes'}, 200


api.add_resource(SignUp, "/register")
api.add_resource(SignIn, "/login")
api.add_resource(ClothesRouter, "/clothes")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)