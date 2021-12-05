from werkzeug.exceptions import NotFound, BadRequest
from decouple import config

from models import Product, TransactionPayment
from schemas import SimpleRequestSchema, SimpleResponseSchema
from db import db
from service import WiseService


class ProductManager:

    @staticmethod
    def get():
        result = Product.query.all()
        schema = SimpleResponseSchema()
        return schema.dump(result, many=True)

    @staticmethod
    def post(data):
        result = Product(**data)
        db.session.add(result)
        db.session.commit()
        schema = SimpleResponseSchema()
        return schema.dump(result)



class ProductInfoManager:

    @staticmethod
    def get(_id):
        result = Product.query.filter_by(id=_id)
        if result.first():
            return result
        raise NotFound("Can't find simple with id {}".format(_id))

    @staticmethod
    def edit(_id, data):
        result = ProductInfoManager.get(_id)
        result.update(data)
        db.session.commit()
        schema = SimpleResponseSchema()
        return schema.dump(result.first())

    @staticmethod
    def delete(_id):
        result = ProductInfoManager.get(_id)
        db.delete(result)
        return 204


class TransactionManager:

    @staticmethod
    def get():
        pass

    @staticmethod
    def post(_id):
        result = ProductInfoManager.get(_id)
        try:
            wise_service = WiseService()
            quote_id = wise_service.create_quote(result.first().price)
            recipient_id = wise_service.create_recipient_account(config('WISE_USER_NAME'), config('IBAN'))
            transfer_id = wise_service.create_transfer(recipient_id, quote_id)
            result.update({"pay": True})
            t = TransactionPayment(pr_id=result.first().id)
            db.session.add(t)
            db.session.commit()
            return {"id": result.first().id, "price": result.first().price, 'transfer': transfer_id}
        except:
            raise ValueError("Error with bank transaction")