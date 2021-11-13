from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, abort
from flask import request
from configurations.models import User, ShopModel
from configurations.schemas import UserShowSchema, UserInputSchema, ShowShopSchema

from werkzeug.security import check_password_hash

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
        return User.query.filter_by(id=user_id).first()
    except Exception:
        abort(400)
        # return 400


class ForTest(Resource):
    def get(self):
        u = User.query.all()
        schema = UserShowSchema(many=True)
        return {"users": schema.dump(u)}, 200

    def post(self):
        data = request.get_json()
        schema = UserInputSchema()
        errors = schema.validate(data)

        if not errors:
            try:
                u = User(**data)
                u.primary_save()
                return {"data": UserShowSchema().dump(data)}, 201
            except ValueError as er:
                return {"error": er}, 400
        return {"Error": str(errors)}


class ShopResourse(Resource):
    @auth.login_required
    def get(self):
        current_user = auth.current_user()
        print(current_user)
        s = ShopModel.query.all()
        schema = ShowShopSchema(many=True)
        return {"products": schema.dump(s)}

    def post(self):
        data = request.get_json()
        schema = ShowShopSchema()
        errors = schema.validate(data)

        if not errors:
            s = ShopModel(**data)
            s.primary_save()
            return {"Success": data['name']}
        return {"Error": errors}


class GetToken(Resource):
    def post(self):
        data = request.get_json()
        schema = UserInputSchema()
        errors = schema.validate(data)

        if not errors:
            u: User= User.find_user_by_email(data['email'])
            if u and check_password_hash(u.password, data['password']):
                token = u.encode_token()
                return {'token': token}, 200
            return {"message": "Credential errors"}, 400

        return {"Error": str(errors)}
