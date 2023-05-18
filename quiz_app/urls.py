from django.urls import path
from quiz_app.views import \
    create_question, get_questions, index, questions_view, \
    leaderboard_view, reset_quiz

urlpatterns = [
    path('', index, name='index'),
    path('create_question/', create_question, name='create_question'),
    path('get_questions/', get_questions, name='get_questions'),
    path('quiz/', questions_view, name='questions_view'),
    path('leaderboard/', leaderboard_view, name='leaderboard_view'),
    path('reset_quiz/', reset_quiz, name='reset_quiz')
]
