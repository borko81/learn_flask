from marshmallow import fields
from models.enum import State
from marshmallow_enum import EnumField
from schemas.base import BaseComplainSchema


class ComplaintResponseSchema(BaseComplainSchema):
    id = fields.Integer(required=True)
    status = EnumField(State, by_value=True)
    create_on = fields.DateTime(required=True)