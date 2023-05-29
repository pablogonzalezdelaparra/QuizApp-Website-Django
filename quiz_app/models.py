# Final Project: Quiz Application with Microservices
# Date: 29-May-2023
# Authors:
# Aleny Sofia Arévalo Magdaleno | A01751272
# Luis Humberto Romero Pérez | A01752789
# Valeria Martínez Silva | A01752167
# Pablo González de la Parra | A01745096
# David Damián Galán | A01752785

from random import sample
from mongoengine import Document, fields
from datetime import datetime


class Quiz(Document):
    """A quiz is a list of questions."""
    questions = fields.ListField(fields.ReferenceField('Question'))
    current_question = fields.IntField(default=0)
    score = fields.IntField(default=0)

    def __init__(self, *args, **kwargs):
        super(Quiz, self).__init__(*args, **kwargs)

    def get_current_question(request):
        """Get the next question in the quiz."""
        question_number = request.session.get('question_number', 1)
        random_question_ids = request.session.get('random_questions', [])
        current_question_id = random_question_ids[question_number - 1]
        question = Question.objects.get(id=current_question_id)
        return question, random_question_ids, \
            question_number, current_question_id

    def get_score(self):
        return self.score

    def retrieve_questions(self, request, num_questions):
        """Retrieve a list of random question
        ids and save them to the session."""
        # Get all question ids
        question_ids = list(Question.objects.values_list('id'))

        # Create a list of random question ids
        random_question_ids = sample(question_ids, int(num_questions))
        random_question_ids = [str(obj_id) for obj_id
                               in random_question_ids]

        # Save random question ids to quiz
        self.questions = random_question_ids

        # Save random question ids to session
        request.session['question_number'] = 1
        request.session['random_questions'] = random_question_ids


class Question(Document):
    """A question is a list of answers."""
    description = fields.StringField(max_length=800)
    answers = fields.ListField(fields.ReferenceField('Answer'))
    feedback = fields.StringField(max_length=800)

    def __init__(self, *args, **kwargs):
        super(Question, self).__init__(*args, **kwargs)

    def get_description(self):
        return str(self.description)

    def get_answers_descriptions(self):
        answers_descriptions = []
        for answer in self.answers:
            answers_descriptions.append(str(answer.description))
        return answers_descriptions

    def check_answer(request, submitted_answer_id, feedback):
        """Check if the answer is correct."""
        if submitted_answer_id:
            submitted_answer = Answer.objects.get(id=submitted_answer_id)
            if submitted_answer.get_is_correct() == 'True':
                feedback = "Correct! " + feedback
                Player.add_score(request)
            else:
                feedback = "Incorrect. " + feedback
            return feedback


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

    def add_score(request):
        """Add 1 to the player's score."""
        player_id = request.session.get('player_id', '')
        player = Player.objects.get(id=player_id)
        player.score += 1
        player.save()

    def get_score(request):
        """Get the player's score."""
        player_id = request.session.get('player_id', '')
        player = Player.objects.get(id=player_id)
        return player.score


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

    def add_player(self, request, username):
        """Create a new player and save their username"""
        # Get username from form
        if (username == ''):
            username = 'Anonymous'

        # Create a new player and save their username and random question ids
        player = Player(username=username)
        player.save()
        self.leaderboard.append(player)
        self.save()

        # Save player id to session
        request.session['player_id'] = str(player.id)

    def get_leaderboard(request):
        players = Player.objects.order_by('-score', '-date')[:10]
        return players
