from db import db


class TransactionPayment(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.Integer, db.ForeignKey('simple.id'))


class Product(db.Model):
    __tablename__ = 'simple'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True, nullable=False)
    price = db.Column(db.Integer, default=1, nullable=False)
    pay = db.Column(db.Boolean, default=False, nullable=False)
    pay_info = db.relationship('TransactionPayment', backref="pay_info", lazy='dynamic')