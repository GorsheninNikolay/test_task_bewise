from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

from test_task.config import Config

# App Flask
app = Flask(__name__)
app.config.from_object(Config)

# Api
api = Api(app)

# DataBase
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)


from . import views
