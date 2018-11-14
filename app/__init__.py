from flask import Flask
from .instance.config import TestConfig, ProductConfig
from flask_jsonrpc import JSONRPC


app = Flask(__name__)
app.config.from_object(TestConfig)
jsonrpc = JSONRPC(app, "/api")


from .handlers import *
