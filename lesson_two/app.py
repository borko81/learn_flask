from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:local60@localhost:5432/flask_su'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db, compare_type=True)
ma = Marshmallow(app)


class UserModel(db.Model):
    __tablename__ = 'myuser'
    email = db.Column(db.String(250), primary_key=True)
    password = db.Column(db.String(250))
    create_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def save(self):
        self.password = generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return self.email


class BookModel(db.Model):
    __tablename__ = 'books'
    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    reader_pk = db.Column(db.Integer, db.ForeignKey('readers.pk'))
    reader = db.relationship('ReaderModel')

    def __repr__(self):
        return f"<{self.pk}> {self.title} from {self.author}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def save(self):
        db.session.add(self)
        db.session.commit()


class ReaderModel(db.Model):
    __tablename__ = 'readers'
    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    books = db.relationship("BookModel", backref="book", lazy='dynamic')


class Books(Resource):
    def post(self):
        data = request.get_json()
        new_book = BookModel(**data)
        new_book.save()
        return new_book.as_dict()

    def get(self):
        books = BookModel.query.all()
        result = BookSchema(many=True)
        # return {"books": [b.as_dict() for b in books]}
        return jsonify(result.dump(books))


class ReaderResourse(Resource):
    def get(self, _id):
        reader = ReaderModel.query.filter_by(pk=_id).first()
        return {"author": reader.first_name, "name": [b.as_dict() for b in reader.books]}


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookModel
        include_relationships = True

api.add_resource(Books, "/")
api.add_resource(ReaderResourse, '/reader/<int:_id>')

if __name__ == '__main__':
    app.run(debug=True)
