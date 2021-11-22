from models.user import UserModel
from flask_restful import Resource
from flask import request
from manager.usermanager import UserManager
from shemas.user_schemas import UserRegisterSchema, UserResponseSchema
from helpers.validated_schemas import validate_schema


class UserRegisterResourse(Resource):
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        schema = UserRegisterSchema()
        return {"token": token}, 201


class UserLoginResourse(Resource):
    @validate_schema(UserRegisterSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {"token": token}


class GetAllUserResourse(Resource):
    def get(self):
        users = UserManager.show_all_users()
        schema = UserResponseSchema()
        result = schema.dump(users, many=True)
        return {"users": result}, 200