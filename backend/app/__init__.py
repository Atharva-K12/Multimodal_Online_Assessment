from flask import Flask
from app.Login.login import login
from app.Student.student import student
from app.Teacher.teacher import teacher
from flask_cors import CORS

def Create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile(config)
    app.register_blueprint(login)
    app.register_blueprint(student)
    app.register_blueprint(teacher)
    print(app.config['SECRET_KEY'])
    return app

