from db import db


class PlaceModel(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    # def __repr__(self) -> str:
    #     return str(self.id)
