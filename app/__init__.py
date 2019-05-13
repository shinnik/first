from flask import Flask
from .instance.config import TestConfig, ProductConfig, SecondTestConfig
from .celery import make_celery
# from .database.create_db import init_db
from flask_jsonrpc import JSONRPC
# from werkzeug.contrib.cache import MemcachedCache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(SecondTestConfig)
jsonrpc = JSONRPC(app, "/api")
# cache = MemcachedCache(['127.0.0.1:11211'])
celery = make_celery(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


from .handlers import *
from app.database.models import *
from .tasks import *

db.create_all()
