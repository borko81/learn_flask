from db import db
from datetime import datetime


class PricesModel(db.Model):
    __tablename__ = "prices"

    id = db.Column(db.Integer, primary_key=True)
    stay_time = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer)
