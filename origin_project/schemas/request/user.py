from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=4))


class RequestRegisterUserSchema(UserSchema):
    first_name = fields.String(required=True, min_lengst=2, max_length=20)
    last_name = fields.String(required=True, min_lengts=2, max_length=20)
    phone = fields.String(required=True, min_length=8)


class RequestLoginUserSchema(UserSchema):
    pass
