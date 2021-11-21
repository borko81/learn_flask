from flask_restful import Resource

from managers.auth import auth
from managers.complain import ComplaintManager
from models.enum import RoleType
from flask import request

from schemas.request.complain import RequestComplainSchema
from schemas.response.complaint import ComplaintResponseSchema
from utils.decorators import validate_schame


class ComplaintListCreate(Resource):
    @auth.login_required
    @validate_schame(RequestComplainSchema)
    def get(self):
        user = auth.current_user()
        complains = ComplaintManager.get_all_complainer_claims(user)
        return ComplaintResponseSchema().dump(complains, many=True)

    @auth.login_required
    @validate_schame(RequestComplainSchema)
    def post(self):
        complainer = auth.current_user()
        data = request.get_json()
        complain = ComplaintManager.create(data, complainer.id)
        return ComplaintResponseSchema().dump(complain)