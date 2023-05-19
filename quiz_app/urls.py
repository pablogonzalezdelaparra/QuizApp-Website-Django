from django.urls import path
from quiz_app.views import QuizViews

urlpatterns = [
    path('', QuizViews.index, name='index'),
    path('create_question/', QuizViews.create_question,
         name='create_question'),
    path('get_questions/', QuizViews.get_questions, name='get_questions'),
    path('quiz/', QuizViews.questions_view, name='questions_view'),
    path('leaderboard/', QuizViews.leaderboard_view, name='leaderboard_view'),
    path('reset_quiz/', QuizViews.reset_quiz, name='reset_quiz')
]
