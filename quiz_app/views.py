from django.shortcuts import render, redirect
from quiz_app.models import Player, Question, Answer
from random import sample


def index(request):
    if request.method == 'POST':
        question_ids = list(Question.objects.values_list('id'))

        num_questions = request.POST.get('num_questions', 1)
        username = request.POST.get('username', "Anonymous")

        random_question_ids = sample(question_ids, int(num_questions))

        random_question_ids = [str(obj_id) for obj_id in random_question_ids]

        player = Player(username=username)
        player.save()

        request.session['question_number'] = 1
        request.session['player_id'] = str(player.id)
        request.session['random_questions'] = random_question_ids

        return redirect('questions_view')
    else:
        return render(request, 'index.html')


def questions_view(request):
    if request.method == 'POST':
        question_number = request.session.get('question_number', 1)
        random_question_ids = request.session.get('random_questions', [])

        if question_number <= len(random_question_ids):

            current_question_id = random_question_ids[question_number - 1]

            question = Question.objects.get(id=current_question_id)

            submitted_answer = request.POST.get('answer', '')

            answer = question.get_desc_correct_answer()

            if submitted_answer.lower() == answer.lower():
                feedback = "Correct!"
                add_score(request)
            else:
                feedback = "Incorrect!"
            question_number += 1

            request.session['question_number'] = question_number
            return render(request, 'quiz.html', {
                'question': question,
                'question_number': question_number-1,
                'feedback': feedback})
        else:
            player = get_score(request)
            return render(request, 'quiz.html', {
                'player': player})

    else:
        question_number = request.session.get('question_number', 1)
        random_question_ids = request.session.get('random_questions', [])

        current_question_id = random_question_ids[question_number - 1]

        question = Question.objects.get(id=current_question_id)

        question_number += 1

        request.session['question_number'] = question_number
        return render(request, 'quiz.html', {
            'question': question, 'question_number': question_number-1})


def create_question(request):
    answer_descriptions = [
        "Paris",
        "London",
        "Berlin",
        "Madrid"
    ]

    is_correct_flags = [
        True,
        False,
        False,
        False
    ]

    question = Question(description="What is the capital of France?")
    question.save()

    for answer_description, is_correct in zip(answer_descriptions,
                                              is_correct_flags):
        answer = Answer(description=answer_description, is_correct=is_correct)
        answer.save()
        question.answers.append(answer)
        question.save()

    return redirect('get_questions')


def get_questions(request):
    questions = Question.objects.all()
    return render(request, 'questions.html', {'questions': questions})


def add_score(request):
    player_id = request.session.get('player_id', '')
    player = Player.objects.get(id=player_id)
    player.add_score()


def get_score(request):
    player_id = request.session.get('player_id', '')
    player = Player.objects.get(id=player_id)
    return player


def leaderboard_view(request):
    players = Player.objects.order_by('-score')
    return render(request, 'leaderboard.html', {'players': players})
