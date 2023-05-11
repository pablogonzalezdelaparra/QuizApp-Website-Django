from django.urls import path
from quiz_app.views import question_view, create_question, \
    select_number_questions

urlpatterns = [
    # path('myview/', my_view, name='my-view'),
    path('create/', create_question, name='create_question'),
    path('quiz/', question_view, name='question_view'),
    path('select/', select_number_questions, name='select_number_questions'),
]
