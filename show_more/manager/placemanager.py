from flask import jsonify, request
from werkzeug.exceptions import BadRequest
from db import db
from models.placemodel import PlaceModel
from manager.validate_place_exists import validate_place_exists
from shemas.place_schema import PlaceSchema


class PlaceManager:

    @staticmethod
    def register_new_place(data):
        name = data['name']
        if validate_place_exists(name):
            p = PlaceModel(name=name)
            db.session.add(p)
            db.session.flush()
            schema = PlaceSchema()
            return {"Create new place": schema.dump(p)}, 201
        raise BadRequest("Not valid place")

    @staticmethod
    def get_all_place():
        return PlaceModel.query.all()

    @staticmethod
    def get_specific_place(_id):
        place = PlaceModel.query.filter_by(id=_id).first()
        if place:
            schema = PlaceSchema()
            return schema.dump(place)
        raise BadRequest("Not found place with that id")

    @staticmethod
    def put_place(_id):
        data = request.get_json()
        schema = PlaceSchema()
        # p = PlaceModel.query.filter_by(id=_id).update(schema.dump(data))
        # return schema.dump(PlaceModel.query.filter_by(id=_id).first())
        return schema.dump(PlaceModel.query.filter_by(id=_id).update(schema.dump(data)))

    @staticmethod
    def delete_place(_id):
        try:
            p = PlaceModel.query.filter_by(id=_id).first()
            db.session.delete(p)
            return 204
        except Exception:
            raise BadRequest("Not found id")


