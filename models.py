from app import db
from sqlalchemy.dialects.postgresql import JSON


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    image_url = db.Column(db.String())
    answer = db.Column(db.String())

    def __init__(self, description, image_url, answer):
        self.description = description
        self.image_url = image_url
        self.answer = answer

    def __repr__(self):
        return '<id {}>'.format(self.id)
