from django.shortcuts import render, redirect
from quiz_app.models import Player, Question, Answer
from random import sample


def index(request):
    """Display the index page. If the user submits the form, create a list of
    random question ids and save them to the session."""
    if request.method == 'POST':
        # Get all question ids
        question_ids = list(Question.objects.values_list('id'))

        # Get number of questions and username from form
        num_questions = request.POST.get('num_questions', 1)
        username = request.POST.get('username', "Anonymous")

        # Create a list of random question ids
        random_question_ids = sample(question_ids, int(num_questions))
        random_question_ids = [str(obj_id) for obj_id in random_question_ids]

        # Create a new player and save their username and random question ids
        player = Player(username=username)
        player.save()

        # Save player id and random question ids to session
        request.session['question_number'] = 1
        request.session['player_id'] = str(player.id)
        request.session['random_questions'] = random_question_ids

        return redirect('questions_view')
    else:
        return render(request, 'index.html')

# DESCOMENTAR CUANDO SE TERMINE DE PROBAR EL ESTILO


def questions_view(request):
    """Display a question and its answers. If the answer is correct, add 1 to
    the player's score."""
    if request.method == 'POST':
        # Get num of current questions, list of random question ids, and answer
        question_number = request.session.get('question_number', 1)
        random_question_ids = request.session.get('random_questions', [])
        submitted_answer_id = request.POST.get('answer', '')

        # Check if answer is correct
        feedback = check_answer(request, submitted_answer_id)

        # Display question
        if question_number <= len(random_question_ids):
            current_question_id = random_question_ids[question_number - 1]
            question = Question.objects.get(id=current_question_id)
            question_number += 1
            request.session['question_number'] = question_number
            return render(request, 'quiz.html', {
                'question': question,
                'question_number': question_number-1,
                'feedback': feedback})

        # Display final score
        else:
            player = get_score(request)
            return render(request, 'quiz.html', {'player': player,
                                                 'feedback': feedback})

    else:
        question_number = request.session.get('question_number', 1)
        random_question_ids = request.session.get('random_questions', [])

        current_question_id = random_question_ids[question_number - 1]
        question = Question.objects.get(id=current_question_id)

        question_number += 1
        request.session['question_number'] = question_number

        return render(request, 'quiz.html', {
            'question': question,
            'question_number': question_number-1})


def check_answer(request, submitted_answer_id):
    """Check if the answer is correct."""
    if submitted_answer_id:
        submitted_answer = Answer.objects.get(id=submitted_answer_id)
        if submitted_answer.is_correct:
            feedback = "Correct!"
            add_score(request)
        else:
            feedback = "Incorrect!"
    return feedback


def create_question(_request):
    """Create a mock question with 4 answers and save it to the database."""
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
    """Get all questions from the database and display them."""
    questions = Question.objects.all()
    return render(request, 'questions.html', {'questions': questions})


def add_score(request):
    """Add 1 to the player's score."""
    player_id = request.session.get('player_id', '')
    player = Player.objects.get(id=player_id)
    player.add_score()


def reset_quiz(request):
    """Reset the quiz by clearing the session data."""
    request.session.pop('question_number', None)
    request.session.pop('player_id', None)
    request.session.pop('random_questions', None)
    return redirect('index')


def get_score(request):
    """Get the player's score."""
    player_id = request.session.get('player_id', '')
    player = Player.objects.get(id=player_id)
    return player


def leaderboard_view(request):
    # Get the top 10 players ordered by score and date of upload
    players = Player.objects.order_by('-score', '-date')[:10]

    # Create a dictionary to store the scores and upload dates for tie-breaking
    scores = {}

    # Iterate over the players to handle ties and assign a rank
    ranked_players = []
    rank = 1
    for player in players:
        score = player.score

        # Check if there's a tie with the previous player
        if ranked_players and scores[ranked_players[-1].id] == score:
            rank -= 1  # Adjust rank for the tie

        ranked_players.append(player)
        scores[player.id] = score

        player.rank = rank
        rank += 1

    return render(request, 'leaderboard.html', {'players': ranked_players})
