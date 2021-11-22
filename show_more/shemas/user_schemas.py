from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserRegisterSchema(UserSchema):
    privileg = fields.String()


class UserResponseSchema(Schema):
    email = fields.Email(required=True)
    privileg = fields.String()