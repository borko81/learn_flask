from db import db
from datetime import datetime


class ParkModel(db.Model):
    __tablename__ = "park"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    get_in = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    get_out = db.Column(db.DateTime, default=None, nullable=True)
    tax = db.Column(db.Integer, default=None, nullable=True)
    pay = db.Column(db.Boolean, default=False)
