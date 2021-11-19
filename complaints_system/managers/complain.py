from db import db
from models.complain import ComplaintModel


class ComplaintManager:
    @staticmethod
    def get_all_complainer_claims(user):
        if isinstance(user, ComplaintModel):
            return ComplaintModel.query.filter_by(complainer_id=user.id).all()
        return ComplaintModel.query.all()

    @staticmethod
    def create(data, complainer_id):
        data['complainer_id'] = complainer_id
        c = ComplaintModel(**data)
        db.session.add(c)
        db.session.flush()
        return c