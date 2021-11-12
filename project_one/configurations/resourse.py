from flask_restful import Resource
from flask import request
from configurations.models import User, ShopModel
from configurations.schemas import UserShowSchema, UserInputSchema, ShowShopSchema
from configurations import auth
from werkzeug.security import check_password_hash



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
                return {"message": "OK", 'token': token}, 200
            return {"message": "Credential errrors"}, 400

        return {"Error": str(errors)}
