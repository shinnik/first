from flask import Flask
from .instance.config import TestConfig, ProductConfig


app = Flask(__name__)
app.config.from_object(TestConfig)

from .views import *
