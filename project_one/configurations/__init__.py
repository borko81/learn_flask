from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from datetime import timedelta
import os
from flask_httpauth import HTTPTokenAuth

basedir = os.path.join(os.path.dirname(__file__), 'app.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret key"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config['DEBUG'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
api = Api(app)
auth = HTTPTokenAuth(scheme='Bearer')

from configurations import models
