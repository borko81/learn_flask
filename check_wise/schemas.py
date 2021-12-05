from marshmallow import Schema, fields, validate


class SimpleRequestSchema(Schema):
    name = fields.String(validate=validate.Length(max=50), required=True)
    price = fields.Integer(required=False)


class SimpleResponseSchema(SimpleRequestSchema):
    id = fields.Integer()
    pay = fields.Boolean()