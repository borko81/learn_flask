from models.user import UserModel


def validate_exists_email(_email):
    return UserModel.query.filter_by(email=_email).first() is None