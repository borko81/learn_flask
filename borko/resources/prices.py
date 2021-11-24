from flask import request
from flask_restful import Resource

from managers.price import PriceManager, PriceConcretManager
from schemas.prices import RequestPriceSchema
from utils.schema_decorator import validate_schema


class PriceRes(Resource):
    @staticmethod
    def get():
        """
        Return all prices
        :return: json data
        USAGE: curl 127.0.0.1:5000/price
        """
        return PriceManager.get_prices()

    @validate_schema(RequestPriceSchema)
    def post(self):
        """
        Post new price in table price
        curl 127.0.0.1:5000/price -X POST -H 'Content-Type: application/json' -d '{"stay_time": "00:03:01", "price": 4}'
        """
        data = request.get_json()
        return PriceManager.add_new_price(data)


class PriceConcretRes(Resource):
    def get(self, _id):
        return PriceConcretManager.get_concrete_price(_id)

    def put(self, _id):
        data = request.get_json()
        return PriceConcretManager.update_concret_price(_id, data)

