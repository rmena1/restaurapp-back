import os
from waitress import serve
from flask import Flask
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev',
)

CORS(app)

from . import routes
app.register_blueprint(routes.bp)

if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get('PORT', 4000))
    serve(app, port=port)
