from marshmallow import Schema, fields, validate, ValidationError
from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    uppercase=1
)

def validate_first_letter(value):
    target = value[0]
    if not target == target.upper():
        raise ValidationError("First char must be upper case")

def validate_password(value):
    error = policy.test(value)
    if error:
        raise ValidationError("Password is not correct!")


class UserInputSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.And(validate_password))


class UserShowSchema(Schema):
    email = fields.Email()


class ShowShopSchema(Schema):
    name = fields.String(required=True, validate=validate.And(validate_first_letter))