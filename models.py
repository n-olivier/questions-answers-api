from app import db


class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, name, description):
        self.name = name
        self.description = description


class JsonModel(object):
    def as_dict(self):
        return {c.name}


class Subtopic(db.Model):
    __tablename__ = 'subtopics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    topic = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)

    def __init__(self, name, description, topic):
        self.name = name
        self.description = description
        self.topic = topic


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    image_url = db.Column(db.String())
    answer = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    subtopic = db.Column(db.Integer, db.ForeignKey('subtopics.id'), nullable=False)

    def __init__(self, description, image_url, answer, subtopic):
        self.description = description
        self.image_url = image_url
        self.answer = answer
        self.subtopic = subtopic

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(), nullable=False)

    def __init__(self, answer):
        self.answer = answer

    def __repr__(self):
        return f"Answer('{self.id}', '{self.answer}')"
