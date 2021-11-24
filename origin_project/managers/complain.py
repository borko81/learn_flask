from db import db
from models.complaint import ComplaintModel
from models.enum import State


class ComplaintManager:
    @staticmethod
    def get_all_complainer_claims(user):
        if isinstance(user, ComplaintModel):
            return ComplaintModel.query.filter_by(
                complainer_id=user.id
            ).first()
        return ComplaintModel.query.all()

    @staticmethod
    def create(data, complainer_id):
        data["complainer_id"] = complainer_id
        c = ComplaintModel(**data)
        db.session.add(c)
        db.session.flush()
        return c

    @staticmethod
    def approve(id_):
        ComplaintModel.query.filter_by(id=id_).update({'status': State.approved})

    @staticmethod
    def reject(id_):
        ComplaintModel.query.filter_by(id=id_).update({'status': State.rejected})