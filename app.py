import os
import random
import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Question, Answer, Topic, Subtopic


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('404.html')


@app.route('/<whatever>')
def display_question(whatever):
    return "Sorry, we don't understand your request!"


@app.route('/questions/new', methods=['GET', 'POST'])
def new_question():
    results = {}
    errors = []
    if request.method == 'POST':
        try:
            # Save answer before to get its id
            answer = Answer(request.form['answer'])
            db.session.add(answer)
            db.session.commit()

            desc = request.form['description']
            image = request.form['image']
            subtopic = request.form['subtopic']

            q = Question(desc, image, answer.id, subtopic)

            db.session.add(q)
            db.session.commit()

        except requests.ConnectionError:
            errors.append(
                "Unable to process your input"
            )

    return render_template(
        'add_question.html', errors=errors, results=results
    )


@app.route('/topics/new', methods=['GET', 'POST'])
def new_topic():
    errors = []
    results = {}
    if request.method == 'POST':

        try:
            name = request.form['name']
            description = request.form['description']

            t = Topic(name, description)

            db.session.add(t)
            db.session.commit()

        except requests.ConnectionError:
            errors.append("Unable to process your input")

    return render_template('add_topic.html', errors=errors, results=results)


@app.route('/subtopics/new', methods=['GET', 'POST'])
def new_subtopic():
    errors = []
    results = {}
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            topic = request.form['topic']

            st = Subtopic(name, description, topic)

            db.session.add(st)
            db.session.commit()

        except requests.ConnectionError:
            errors.append("Unable to process your input")

    return render_template('add_subtopic.html', errors=errors, results=results)


# fetch all topics available
class Topics(Resource):
    @staticmethod
    def get():
        results = []
        try:
            topics = Topic.query.all()

            for topic in topics:
                results.append(
                    {
                        'name': topic.name,
                        'description': topic.description
                    }
                )

            return results

        except ConnectionError:
            return {'error': "Unable to fetch from database"}


api.add_resource(Topics, '/topics/all')


# fetch subtopics depending on a topic
class Subtopics(Resource):
    @staticmethod
    def get(topic_id):
        results = []
        try:
            subtopics = Subtopic.query.filter_by(topic=topic_id).all()

            for subtopic in subtopics:
                results.append(
                    {
                        'name': subtopic.name,
                        'description': subtopic.description
                    }
                )

            return results

        except ConnectionError:
            return {'error': "Unable to fetch from database"}


api.add_resource(Subtopics, '/subtopics/<topic_id>')


# random question
class RandomQuestion(Resource):
    @staticmethod
    def get(subtopic_id):
        try:
            questions = Question.query.filter_by(subtopic=subtopic_id).all()

            q = random.randint(0, len(questions) - 1)

            return {'topic': questions[q].subtopic,
                    'question': questions[q].description,
                    'image': questions[q].image_url,
                    'answer': Answer.query.filter_by(id=questions[q].answer).first().answer
                    }

        except ConnectionError:
            return {'error': "Unable to fetch from database"}


api.add_resource(RandomQuestion, '/questions/random/<subtopic_id>')


# writing to database

# add a question


if __name__ == '__main__':

    app.run()

