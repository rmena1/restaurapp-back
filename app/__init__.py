import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev',
)

CORS(app)

from . import routes
app.register_blueprint(routes.bp)
