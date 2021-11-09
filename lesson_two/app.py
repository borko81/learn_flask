from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import datetime
import os
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("USER_NAME_FOR_DB")}:{os.getenv("PASSWORD_FOR_DB")}@{os.getenv("HOST_DB")}:5432/{os.getenv("PATH_TO_BASE")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)



class TestModel(db.Model):
    __tablename__ = 'testtable'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('myuser.id'))
    user_email = db.Column(db.String(250), default=None)
    income = db.Column(db.DateTime, default=datetime.datetime.today())
    outcome = db.Column(db.DateTime, nullable=True)
    price = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return str(self.id)

    def save(self):
        if self.outcome:
            self.price = 1
        self.user_email = UserModel.query.filter_by(id=self.user_id).first().email
        db.session.add(self)
        db.session.commit()


class UserModel(db.Model):
    __tablename__ = 'myuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(250))
    create_on = db.Column(db.DateTime, default=datetime.datetime.now())
    test_ref = db.relationship('TestModel', lazy='dynamic', backref='test_ref')

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
    reader = db.relationship('ReaderModel', backref='reader')

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
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String, nullable=False)


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


class UserSchema(ma.Schema):
    class Meta:
        model = UserModel
        fields = 'id email create_on'.split()


class UserResourse(Resource):
    def get(self):
        user = UserModel.query.first()
        schema = UserSchema()
        return schema.dump(user)


class TestModelResourse(Resource):
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('myuser.id'))
    user_email = db.Column(db.String(250), default=None)
    income = db.Column(db.DateTime, default=datetime.datetime.today())
    outcome = db.Column(db.DateTime, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    """
    resourse_field = {
        "id": fields.Integer,
        "user_id": fields.Integer,
        "user_email": fields.String
    }

    @marshal_with(resourse_field)
    def get(self):
        result = TestModel.query.one()
        return result


api.add_resource(Books, "/")
api.add_resource(ReaderResourse, '/reader/<int:_id>')
api.add_resource(UserResourse, '/users')
api.add_resource(TestModelResourse, '/test')

if __name__ == '__main__':
    app.run(debug=True)
