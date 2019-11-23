import os
import random
import requests
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Question, Answer, Topic, Subtopic


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify(error=404, text=str(e)), 404


@app.route('/questions/new', methods=['POST'])
def new_question():
    try:
        content = request.get_json()
        description = content['description']
        image_url = content['image_url']
        answer = content['answer']
        subtopic = content['subtopic']

        # Save answer before to get its id
        answer = Answer(answer)
        db.session.add(answer)
        db.session.commit()

        q = Question(description, image_url, answer.id, subtopic)

        db.session.add(q)
        db.session.commit()

        return '', 200

    except requests.HTTPError:
        return '', 400


@app.route('/topics/new', methods=['POST'])
def new_topic():
    try:
        content = request.get_json()
        name = content['name']
        description = content['description']

        t = Topic(name, description)

        db.session.add(t)
        db.session.commit()

        return '', 200

    except requests.HTTPError:
        return '', 400


@app.route('/subtopics/new', methods=['POST'])
def new_subtopic():
    try:
        content = request.get_json()
        name = content['name']
        description = content['description']
        topic = content['topic']

        st = Subtopic(name, description, topic)

        db.session.add(st)
        db.session.commit()

        return '', 200

    except requests.HTTPError:
        return '', 400


# fetch all topics available
class TopicsList(Resource):
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


api.add_resource(TopicsList, '/topics/all')


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

if __name__ == '__main__':
    app.run()
