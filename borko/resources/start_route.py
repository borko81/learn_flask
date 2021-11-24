from flask_restful import Resource
from managers.price import PriceManager


class FirstRoute(Resource):
    def get(self):
        return {"message": "Server is online"}, 200


class GetAllPRices(Resource):
    def get(self):
        return PriceManager.get_prices()
