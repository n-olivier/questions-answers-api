import os
from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<qId>')
def display_question(qId):
    return "The question is {}.".format(qId)


if __name__ == '__main__':
    app.run()

print(os.environ['APP_SETTINGS'])
