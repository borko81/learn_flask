from models.placemodel import PlaceModel


def validate_place_exists(_place):
    return PlaceModel.query.filter_by(name=_place).first() is None