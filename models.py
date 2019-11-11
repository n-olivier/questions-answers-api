from app import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    image_url = db.Column(db.String())
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)

    def __init__(self, description, image_url, answer_id):
        self.description = description
        self.image_url = image_url
        self.answer_id = answer_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Answer('{self.id}', '{self.answer}')"


