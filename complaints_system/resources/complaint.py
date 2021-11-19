from flask_restful import Resource

from managers.auth import auth
from managers.complain import ComplaintManager
from models.enum import RoleType
from flask import request

from schemas.request.complain import RequestComplainSchema
from schemas.response.complain import ComplaintResponseSchema
from utils.validate_schemas import permission_required, validate_schema



class CompplaintListCreate(Resource):
    @auth.login_required
    @validate_schema(RequestComplainSchema)
    def get(self):
        user = auth.current_user()
        complains = ComplaintManager.get_all_complainer_claims(user)
        return ComplaintResponseSchema().dump(complains, many=True)

    @auth.login_required
    @validate_schema(RequestComplainSchema)
    def post(self):
        complainer = auth.current_user()
        data = request.get_json()
        complaint = ComplaintManager.create(data, complainer.id)
        return ComplaintResponseSchema().dump(complaint)