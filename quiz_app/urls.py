# Final Project: Quiz Application with Microservices
# Date: 29-May-2023
# Authors:
# Aleny Sofia Arévalo Magdaleno | A01751272
# Luis Humberto Romero Pérez | A01752789
# Valeria Martínez Silva | A01752167
# Pablo González de la Parra | A01745096
# David Damián Galán | A01752785

from django.urls import path
from quiz_app.views import QuizViews

urlpatterns = [
    path('', QuizViews.index, name='index'),
    path('quiz/', QuizViews.questions_view, name='questions_view'),
    path('leaderboard/', QuizViews.leaderboard_view, name='leaderboard_view'),
    path('reset_quiz/', QuizViews.reset_quiz, name='reset_quiz')
]
