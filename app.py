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


@app.route('/<q_id>')
def display_question(q_id):
    return "The question is {}.".format(q_id)


if __name__ == '__main__':
    app.run()

