from db import db
from models.prices import PricesModel
from schemas.prices import RequestPriceSchema, ResponsePRiceScema, RequestPriceSchema


class PriceManager:

    @staticmethod
    def get_prices():
        schema = ResponsePRiceScema()
        return {"prices": schema.dump(PricesModel.query.all(), many=True)}

    @staticmethod
    def add_new_price(data):
        schema = RequestPriceSchema()
        p = PricesModel(**data)
        db.session.add(p)
        db.session.flush()
        return schema.dump(p)


class PriceConcretManager:

    @staticmethod
    def get_from_id(_id):
        p = PricesModel.query.filter_by(id=_id)
        return p

    @staticmethod
    def get_concrete_price(_id):
        p = PriceConcretManager.get_from_id(_id).first()
        schema = RequestPriceSchema()
        return schema.dump(p), 200

    @staticmethod
    def update_concret_price(_id, data):
        p = PriceConcretManager.get_from_id(_id)
        schema = RequestPriceSchema()
        p.update(schema.dump(data))
        schema = RequestPriceSchema()
        return schema.dump(p.first()), 200