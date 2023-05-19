from mongoengine import Document, fields
from datetime import datetime


class Quiz(Document):
    """A quiz is a list of questions."""
    questions = fields.ListField(fields.ReferenceField('Question'))
    current_question = fields.IntField(default=0)
    score = fields.IntField(default=0)

    def __init__(self, *args, **kwargs):
        super(Quiz, self).__init__(*args, **kwargs)

    def get_current_question(self):
        return self.questions[self.current_question]

    def answer_current_question(self, answer_id):
        if answer_id == self.get_current_question().get_id_correct_answer():
            self.score += 1
        self.current_question += 1
        self.save()

    def get_score(self):
        return self.score


class Question(Document):
    """A question is a list of answers."""
    description = fields.StringField(max_length=200)
    answers = fields.ListField(fields.ReferenceField('Answer'))

    def __init__(self, *args, **kwargs):
        super(Question, self).__init__(*args, **kwargs)

    def get_description(self):
        return str(self.description)

    def get_answers_descriptions(self):
        answers_descriptions = []
        for answer in self.answers:
            answers_descriptions.append(str(answer.description))
        return answers_descriptions

    def get_id_correct_answer(self):
        for answer in self.answers:
            if answer.is_correct:
                return answer.id


class Answer(Document):
    """An answer is a description and a flag to indicate if it is correct."""
    description = fields.StringField(max_length=200)
    is_correct = fields.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Answer, self).__init__(*args, **kwargs)

    def get_description(self):
        return str(self.description)

    def get_is_correct(self):
        return str(self.is_correct)


class Player(Document):
    """A player is a username and a score."""
    date = fields.DateTimeField(default=datetime.now)
    username = fields.StringField(max_length=200)
    score = fields.IntField(default=0)

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

    def add_score(self):
        self.score += 1
        self.save()


class QuizService(Document):
    """A quiz service is a list of quizzes."""
    quizzes = fields.ListField(fields.ReferenceField('Quiz'))

    def __init__(self, *args, **kwargs):
        super(QuizService, self).__init__(*args, **kwargs)

    def get_quiz(self, quiz_id):
        return self.quizzes[quiz_id]


class Leaderboard(Document):
    """A leaderboard is a list of players."""
    leaderboard = fields.ListField(fields.ReferenceField('Player'))

    def __init__(self, *args, **kwargs):
        super(Leaderboard, self).__init__(*args, **kwargs)

    def add_player(self, player):
        self.leaderboard.append(player)
        self.save()

    def get_leaderboard(self):
        return self.leaderboard
