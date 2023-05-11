from mongoengine import Document, fields


'''
class MyModel(Document):
    name = fields.StringField(max_length=50)
    description = fields.StringField(max_length=200)
'''


class Question(Document):
    question_text = fields.StringField(max_length=200)
    answer = fields.StringField(max_length=100)
