from flask import Flask
from app.Login.login import login
from flask_cors import CORS

def Create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile(config)
    app.register_blueprint(login)
    return app

