from flask_restful import Resource
from flask import request
from managers.user import ComplainerManager
from schemas.request.user import RequestRegisterSchema, RequestLoginUserSchema
from utils.validate_schemas import validate_schema


class RegisterComplainer(Resource):
    @validate_schema(RequestRegisterSchema)
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