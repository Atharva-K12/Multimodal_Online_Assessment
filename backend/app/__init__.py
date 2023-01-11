from flask import Flask
from app.Login.login import login

def Create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    app.register_blueprint(login)
    return app

