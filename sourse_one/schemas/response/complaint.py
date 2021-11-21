from marshmallow import Schema, fields

class ComplaintResponseSchema(Schema):
    id = fields.Integer(required=True)
    status = fields.String(required=True)
    create_on = fields.DateTime(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    photo_url = fields.String(required=True)
    amount = fields.Float(required=True)