from django.shortcuts import render, redirect
from quiz_app.models import Question
import json
from random import sample


'''
def my_view(request):
    # Create a new instance of MyModel
    my_model = MyModel(name='Example', description='This is an example')

    # Save the instance to the database
    my_model.save()

    # Retrieve all instances from the database
    all_models = MyModel.objects.all()

    return render(request, 'my_template.html', {'models': all_models})
'''


def create_question(request):
    # Create a new instance of MyModel
    my_model = Question(question_text='Question!!!',
                        answer='This is an example')

    # Save the instance to the database
    my_model.save()

    # Retrieve all instances from the database
    all_models = Question.objects.all()

    return render(request, 'my_template.html', {'models': all_models})


def select_number_questions(request):
    if request.method == 'POST':
        # Retrieve all question IDs from the database
        question_ids = list(Question.objects.values_list('id'))

        # Get the number of questions from the form
        num_questions = request.POST.get('num_questions', 1)

        # Sample 'n' random question IDs
        random_question_ids = sample(question_ids, int(num_questions))

        # Convert ObjectIds to strings for filtering
        random_question_ids = [str(obj_id) for obj_id in random_question_ids]

        # First question, initialize the question number in the session
        request.session['question_number'] = 1
        request.session['random_questions'] = random_question_ids

        return redirect('question_view')
    else:
        return render(request, 'select_number_questions.html')


def question_view(request):
    if request.method == 'POST':
        question_number = request.session.get('question_number', 1)
        random_question_ids = request.session.get('random_questions', [])

        # Retrieve the current question ID from the list based on the
        # question number
        current_question_id = random_question_ids[question_number - 1]

        # Retrieve the question from the database based on the current
        # question ID
        question = Question.objects.get(id=current_question_id)

        # Get the submitted answer from the form
        submitted_answer = request.POST.get('answer', '')

        # Compare the submitted answer with the correct answer
        if submitted_answer.lower() == question.answer.lower():
            # Correct answer
            feedback = "Correct!"
        else:
            # Incorrect answer
            feedback = "Incorrect!"

        # Increment the question number for the next question
        question_number += 1

        # Store the updated question number in the session
        request.session['question_number'] = question_number

        # Check if there are more questions or if the quiz is complete
        if question_number <= len(random_question_ids):
            return render(request, 'quiz.html', {'question': question, 'feedback': feedback})
        else:
            # Quiz completed, redirect to a completion page or another view
            return render(request, 'quiz.html')

    else:
        question_number = request.session.get('question_number', 1)
        random_question_ids = request.session.get('random_questions', [])
        print("random_question_ids: ", random_question_ids)

        # Retrieve the current question ID from the list based on the
        # question number
        current_question_id = random_question_ids[question_number - 1]

        # Retrieve the question from the database based on the current
        # question ID
        question = Question.objects.get(id=current_question_id)

        question_number += 1

        # Store the updated question number in the session
        request.session['question_number'] = question_number
        return render(request, 'quiz.html', {'question': question})
