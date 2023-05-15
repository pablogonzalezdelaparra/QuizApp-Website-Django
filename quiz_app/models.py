from mongoengine import Document, fields
from datetime import datetime


class Question(Document):
    description = fields.StringField(max_length=200)
    answers = fields.ListField(fields.ReferenceField('Answer'))

    def get_desc_correct_answer(self):
        for answer in self.answers:
            if answer.is_correct:
                return str(answer.description)


class Answer(Document):
    description = fields.StringField(max_length=200)
    is_correct = fields.BooleanField(default=False)


class Player(Document):
    date = fields.DateTimeField(default=datetime.now)
    username = fields.StringField(max_length=200)
    score = fields.IntField(default=0)

    def add_score(self):
        self.score += 1
        self.save()
