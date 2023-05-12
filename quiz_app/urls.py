from django.urls import path
from quiz_app.views import \
    create_question, get_questions, index, questions_view

urlpatterns = [
    path('', index, name='index'),
    path('create_question/', create_question, name='create_question'),
    path('get_questions/', get_questions, name='get_questions'),
    path('quiz/', questions_view, name='questions_view'),
]
