from mongoengine import Document, fields


class Question(Document):
    description = fields.StringField(max_length=200)
    answers = fields.ListField(fields.ReferenceField('Answer'))

    def get_id_correct_answer(self):
        for answer in self.answers:
            if answer.is_correct:
                return answer.id


class Answer(Document):
    description = fields.StringField(max_length=200)
    is_correct = fields.BooleanField(default=False)
