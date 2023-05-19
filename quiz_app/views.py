from django.shortcuts import render, redirect
from quiz_app.models import Player, Question, Answer
from random import sample


class QuizViews:
    def index(request):
        """Display the index page. If the user submits the form, create a list
        of random question ids and save them to the session."""
        if request.method == 'POST':
            # Get number of questions and username from form
            num_questions = request.POST.get('num_questions', 1)
            username = request.POST.get('username')

            # Create a list of random question ids and save them to the session
            QuizViews.retrieve_questions(request, num_questions)

            # Create a new player and save their username
            QuizViews.create_user(request, username)

            # Redirect to the quiz page
            return redirect('questions_view')
        else:
            # Display the index page
            return render(request, 'index.html')

    def questions_view(request):
        """Display a question and its answers. If the answer is correct,
        add 1 to the player's score."""
        if request.method == 'POST':
            # Get next question
            question_number = request.session.get('question_number', 1)
            random_question_ids = request.session.get('random_questions', [])

            # Get submitted answer
            submitted_answer_id = request.POST.get('answer')

            if submitted_answer_id is None:
                # Display message if no answer is selected
                feedback = "Please select an answer."
                return render(request, 'quiz.html', {
                    'question': question,
                    'question_number': question_number-1,
                    'feedback': feedback})
            else:
                # Check if answer is correct
                feedback = QuizViews.check_answer(request, submitted_answer_id)

                # Display question
                if question_number <= len(random_question_ids):
                    # Get next question
                    current_question_id = random_question_ids[
                        question_number - 1]
                    question = Question.objects.get(id=current_question_id)
                    question_number += 1
                    request.session['question_number'] = question_number
                    return render(request, 'quiz.html', {
                        'question': question,
                        'question_number': question_number-1,
                        'feedback': feedback})

                # Display final score
                else:
                    player_score = QuizViews.get_score(request)
                    return render(request, 'quiz.html', {
                        'player': player_score,
                        'feedback': feedback})

        else:
            # Get next question
            question, random_question_ids, question_number, \
                current_question_id = QuizViews.get_next_question(request)

            # Increment question number
            question_number += 1
            request.session['question_number'] = question_number

            # Display question
            return render(request, 'quiz.html', {
                'question': question,
                'question_number': question_number-1})

    def leaderboard_view(request):
        """Display the leaderboard."""
        # Get the top 10 players ordered by score and date of upload
        players = Player.objects.order_by('-score', '-date')[:10]

        # Create a dictionary to store the scores and
        # upload dates for tie-breaking
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

    # Auxiliary methods
    def retrieve_questions(request, num_questions):
        """Retrieve a list of random question
        ids and save them to the session."""
        # Get all question ids
        question_ids = list(Question.objects.values_list('id'))

        # Create a list of random question ids
        random_question_ids = sample(question_ids, int(num_questions))
        random_question_ids = [str(obj_id) for obj_id
                               in random_question_ids]

        # Save random question ids to session
        request.session['question_number'] = 1
        request.session['random_questions'] = random_question_ids

    def create_user(request, username):
        """Create a new player and save their username"""

        # Get username from form
        if (username == ''):
            username = 'Anonymous'

        # Create a new player and save their username and random question ids
        player = Player(username=username)
        player.save()

        # Save player id to session
        request.session['player_id'] = str(player.id)

    def get_next_question(request):
        """Get the next question in the quiz."""
        question_number = request.session.get('question_number', 1)
        random_question_ids = request.session.get('random_questions', [])
        current_question_id = random_question_ids[question_number - 1]
        question = Question.objects.get(id=current_question_id)
        return question, random_question_ids, \
            question_number, current_question_id

    def check_answer(request, submitted_answer_id):
        """Check if the answer is correct."""
        if submitted_answer_id:
            submitted_answer = Answer.objects.get(id=submitted_answer_id)
            if submitted_answer.is_correct:
                feedback = "Correct!"
                QuizViews.add_score(request)
            else:
                feedback = "Incorrect!"
        return feedback

    def create_question(_request):
        """Create a mock question with 4 answers and
        save it to the database."""
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
            answer = Answer(description=answer_description,
                            is_correct=is_correct)
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
        return player.score
