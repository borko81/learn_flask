from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Resource, Api

from db import db
from manager import *
from decorators import validate_schema
from schemas import SimpleRequestSchema

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
migrate = Migrate(app, db, compare_type=True)
db.init_app(app)


class ProductResourse(Resource):
    @staticmethod
    def get():
        return ProductManager.get(), 200

    @validate_schema(SimpleRequestSchema)
    def post(self):
        data = request.get_json()
        return ProductManager.post(data), 201


class ProductInfoResourse(Resource):
    @staticmethod
    def get(_id):
        schema = SimpleResponseSchema()
        return schema.dump(ProductInfoManager.get(_id).first())

    def put(self, _id):
        data = request.get_json()
        return ProductInfoManager.edit(_id, data)

    @staticmethod
    def delete(_id):
        return ProductInfoManager.delete(_id)


class TransactionResourse(Resource):

    @staticmethod
    def get():
        return TransactionManager.get()

    @staticmethod
    def post(_id):
        return TransactionManager.post(_id)


api.add_resource(ProductResourse, '/simple')
api.add_resource(ProductInfoResourse, '/simple/<int:_id>')
api.add_resource(TransactionResourse, '/transaction/<int:_id>')

if __name__ == "__main__":
    app.run(debug=True)
