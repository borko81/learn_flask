from marshmallow import Schema, fields


class ParkEnterSchema(Schema):
    name = fields.String(required=True)


class ParkResponseSchema(ParkEnterSchema):
    id = fields.Integer()
    get_in = fields.String()


class ParkWhoAlreadyOut(ParkResponseSchema):
    get_out = fields.String()
    tax = fields.String()
    pay = fields.Boolean()
