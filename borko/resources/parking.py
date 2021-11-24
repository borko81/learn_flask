from flask import request
from flask_restful import Resource

from managers.parking import ParkingManager
from schemas.parking import ParkEnterSchema
from utils.schema_decorator import validate_schema


class ParkRes(Resource):
    @validate_schema(ParkEnterSchema)
    def post(self):
        data = request.get_json()
        return ParkingManager.input_new_car_in_park(data), 201

    def get(selfO):
        return ParkingManager.show_car_in_park(), 200
