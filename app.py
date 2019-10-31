import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Question


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<qId>')
def display_question(qId):
    return "The question is {}.".format(qId)


if __name__ == '__main__':
    app.run()

