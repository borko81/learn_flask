from flask_restful import Resource
from flask import request
from managers.user import ComplainerManager
from schemas.request.user import RequestRegisterSchema, RequestLoginUserSchema, UserSchema
from utils.decorators import validate_schame


class RegisterComplainer(Resource):
    @validate_schame(RequestRegisterSchema)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {"token": token}, 201


class LoginComplainer(Resource):
    @validate_schame(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.login(data)
        return {"token": token, "role": "complainer"}