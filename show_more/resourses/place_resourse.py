from flask import request
from flask_restful import Resource
from helpers.validated_schemas import validate_schema
from manager.placemanager import PlaceManager
from shemas.place_schema import PlaceSchema


class PlaceResourse(Resource):

    @validate_schema(PlaceSchema)
    def post(self):
        data = request.get_json()
        p = PlaceManager.register_new_place(data)
        return p

    def get(self):
        places = PlaceManager.get_all_place()
        schema = PlaceSchema()
        return {"all_places": schema.dump(places, many=True)}, 200


class PlaceSpecificResourse(Resource):
    def get(self, _id):
        place = PlaceManager.get_specific_place(_id)
        return place

    @validate_schema(PlaceSchema)
    def put(self, _id):
        return PlaceManager.put_place(_id)

    def delete(self, _id):
        return PlaceManager.delete_place(_id)
