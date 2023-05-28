from django.urls import path
from quiz_app.views import QuizViews

urlpatterns = [
    path('', QuizViews.index, name='index'),
    path('quiz/', QuizViews.questions_view, name='questions_view'),
    path('leaderboard/', QuizViews.leaderboard_view, name='leaderboard_view'),
    path('reset_quiz/', QuizViews.reset_quiz, name='reset_quiz')
]
