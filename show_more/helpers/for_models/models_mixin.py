from db import db


class MixinModel(object):
    query = None
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)

    @classmethod
    def get_from_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def get_from_email(cls, user_email):
        return cls.query.filter_by(email=user_email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()