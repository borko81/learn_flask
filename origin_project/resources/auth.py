from flask_restful import Resource
from flask import request
from managers.user import ComplainerManager
from utils.decorators import validate_schema
from schemas.request.user import RequestRegisterUserSchema, RequestLoginUserSchema


class RegisterComplainer(Resource):
    @validate_schema(RequestRegisterUserSchema)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {"token": token}, 201


class LoginComplainer(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.login(data)
        return {"token": token, "role": "complainer"}
