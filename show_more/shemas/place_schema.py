from marshmallow import Schema, fields, validate


def validate_name_of_place(value):
    return any(char.isdigit() for char in value)


class PlaceIDSchema(Schema):
    id = fields.Integer(required=False)


class PlaceSchema(PlaceIDSchema):
    name = fields.String(min_length=2, required=True, validate=validate.And(validate_name_of_place))
