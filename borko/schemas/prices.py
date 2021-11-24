from marshmallow import Schema, fields, validate


class RequestPriceSchema(Schema):
    stay_time = fields.String(required=True)
    price = fields.Integer(required=True)


class ResponsePRiceScema(RequestPriceSchema):
    id = fields.Integer()