from django.shortcuts import render, redirect
from quiz_app.models import Player, Question, Answer, Quiz, \
    QuizService, Leaderboard


class QuizViews:
    def index(request):
        """Display the index page. If the user submits the form, create a list
        of random question ids and save them to the session."""
        if request.method == 'POST':
            # Get number of questions and username from form
            num_questions = request.POST.get('num_questions', 1)
            username = request.POST.get('username')

            # Create a new Quiz instance
            quiz = Quiz()
            quiz.save()

            # Retrieve a list of random question ids and save \
            # them to the Quiz instance
            quiz.retrieve_questions(request, num_questions)

            leaderboard = Leaderboard()
            leaderboard.save()

            # Create a new player and save their username
            leaderboard.add_player(request, username)

            # Redirect to the quiz page
            return redirect('questions_view')
        else:
            # Run only the first time. Then comment out.!!!
            # QuizViews.load_questions_in_db(QuizViews)

            # Display the index page
            return render(request, 'index.html')

    def questions_view(request):
        """Display a question and its answers. If the answer is correct,
        add 1 to the player's score."""
        if request.method == 'POST':
            # Get next question
            question_number = request.session.get('question_number', 1)
            random_question_ids = request.session.get('random_questions', [])
            submitted_answer_id = request.POST.get('answer')
            feedback_prev = request.POST.get('feedback')

            if submitted_answer_id is None:
                # Display message if no answer is selected
                feedback = "Please select an answer."
                return render(request, 'quiz.html', {
                    'question': question,
                    'question_number': question_number-1,
                    'feedback': feedback})
            else:
                # Check if answer is correct
                feedback = Question.check_answer(
                    request, submitted_answer_id, feedback_prev)

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
                    player_score = Player.get_score(request)
                    return render(request, 'quiz.html', {
                        'player': player_score,
                        'feedback': feedback})

        else:
            if 'player_id' not in request.session:
                # Redirect to the index page if the player id is not in session
                return redirect('index')
            # Get next question
            question, random_question_ids, question_number, \
                current_question_id = Quiz.get_current_question(request)

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
        players = Leaderboard.get_leaderboard(request)

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

    def reset_quiz(request):
        """Reset the quiz by clearing the session data."""
        request.session.pop('question_number', None)
        request.session.pop('player_id', None)
        request.session.pop('random_questions', None)
        return redirect('index')

    def load_questions_in_db(self):
        # Create a mock question with choices and save it to the database
        question_data = [
            {
                "question": "What does the 'S' in SOLID stand for?",
                "choices": [
                    {"description": "Simple", "is_correct": False},
                    {"description": "Single Responsibility", "is_correct":
                     True},
                    {"description": "Separation of Concerns", "is_correct":
                     False},
                    {"description": "Solidarity", "is_correct": False}
                ],
                "feedback": "The 'S' in SOLID stands for Single \
                    Responsibility Principle."
            },
            {
                "question": "Which SOLID principle suggests that code \
                    should depend on abstractions rather than concrete \
                        implementations?",
                "choices": [
                    {"description": "Open/Closed Principle", "is_correct":
                     False},
                    {"description": "Single Responsibility Principle",
                        "is_correct": False},
                    {"description": "Liskov Substitution Principle",
                        "is_correct": False},
                    {"description": "Dependency Inversion Principle",
                     "is_correct": True}
                ],
                "feedback": "The Dependency Inversion Principle suggests \
                    that code should depend on abstractions rather than \
                        concrete implementations."
            },
            {
                "question": "Which SOLID principle suggests that a class \
                    should implement only the methods it needs?",
                "choices": [
                    {"description": "Open/Closed Principle", "is_correct":
                     False},
                    {"description": "Single Responsibility Principle",
                        "is_correct": False},
                    {"description": "Liskov Substitution Principle",
                        "is_correct": False},
                    {"description": "Interface Segregation Principle",
                        "is_correct": True}
                ],
                "feedback": "The Interface Segregation Principle suggests \
                    that a class should implement only the methods it needs."
            },
            {
                "question": "Which SOLID principle suggests that classes \
                    should be open for extension but closed for modification?",
                "choices": [
                    {"description": "Open/Closed Principle", "is_correct":
                     True},
                    {"description": "Liskov Substitution Principle",
                        "is_correct": False},
                    {"description": "Interface Segregation Principle",
                        "is_correct": False},
                    {"description": "Single Responsibility Principle",
                        "is_correct": False}
                ],
                "feedback": "The Open/Closed Principle suggests that classes \
                    should be open for extension but closed for modification."
            },
            {
                "question": "Which SOLID principle suggests that when \
                    extending a class, the subclasses should remain \
                        compatible with the behavior of the superclass?",
                "choices": [
                    {"description": "Dependency Inversion Principle",
                        "is_correct": False},
                    {"description": "Open/Closed Principle", "is_correct":
                     False},
                    {"description": "Liskov Substitution Principle",
                     "is_correct": True},
                    {"description": "Single Responsibility Principle",
                        "is_correct": False}
                ],
                "feedback": "The Liskov Substitution Principle suggests \
                    that when extending a class, the subclasses should \
                        remain compatible with the behavior of the superclass."
            },
            {
                "question": "What is an interface in OOP?",
                "choices": [
                    {"description": "A class that cannot be instantiated and \
                     only contains abstract methods", "is_correct": True},
                    {"description": "A subclass that inherits properties and \
                     methods from a parent class",
                     "is_correct": False},
                    {"description": "A way to encapsulate data and behavior \
                     into a single entity",
                     "is_correct": False},
                    {"description": "A set of rules that defines the behavior \
                     of a class",
                     "is_correct": False}
                ],
                "feedback": "An interface in OOP is a class that cannot be \
                    instantiated and only contains abstract methods."
            },
            {
                "question": "In OOP, it refers to the ability to hide parts \
                    of its state or implementation details from other \
                        objects or classes.",
                "choices": [
                    {"description": "Polymorphism", "is_correct": False},
                    {"description": "Inheritance", "is_correct": False},
                    {"description": "Encapsulation", "is_correct": True},
                    {"description": "Abstraction", "is_correct": False}
                ],
                "feedback": "In OOP, encapsulation refers to the ability to \
                    hide parts of its state or implementation details from \
                        other objects or classes."
            },
            {
                "question": "Which of the statements is false about \
                    inheritance in OOP?",
                "choices": [
                    {"description": "The main benefit of inheritance is code \
                     reuse.",
                     "is_correct": False},
                    {"description": "A child class doesn't have to have all \
                     the parents abstract methods implemented", "is_correct":
                     True},
                    {"description": "Is the ability to build new classes on \
                     top of existing ones.",
                     "is_correct": False},
                    {"description": "Reusing code through inheritance can \
                     lead to parallel inheritance hierarchies", "is_correct":
                     False}
                ],
                "feedback": "The statement 'A child class doesn't have to \
                    have all the parents abstract methods implemented' is \
                        false about inheritance in OOP."
            },
            {
                "question": "What is polymorphism in OOP?",
                "choices": [
                    {"description": "The ability to create a new class \
                     from an existing class",
                     "is_correct": False},
                    {"description": "The ability to define multiple methods \
                     with the same name in a class",
                     "is_correct": True},
                    {"description": "The ability to hide implementation \
                     details from other classes",
                     "is_correct": False},
                    {"description": "The ability to inherit properties and \
                     methods from a parent class",
                     "is_correct": False}
                ],
                "feedback": "Polymorphism in OOP refers to the ability to \
                    define multiple methods with the same name in a class."
            },
            {
                "question": "In OOP, when should you use an interface?",
                "choices": [
                    {"description": "When you need to add an extension to \
                     the behavior",
                     "is_correct": False},
                    {"description": "When you already know that a class \
                     will have to be extended to meet a requirement",
                     "is_correct": False},
                    {"description": "When you want to encourage people to \
                     extend in a specific way",
                     "is_correct": False},
                    {"description": "All of the options", "is_correct": True}
                ],
                "feedback": "Interfaces should be used when you want to \
                    encourage people to extend in a specific way, when you \
                        need to add an extension to the behavior, or when \
                            you already know that a class will have to be \
                                extended to meet a requirement."
            },
            {
                "question": "Which of these is not a REST API method?",
                "choices": [
                    {"description": "UPDATE", "is_correct": True},
                    {"description": "GET", "is_correct": False},
                    {"description": "DELETE", "is_correct": False},
                    {"description": "POST", "is_correct": False}
                ],
                "feedback": "'UPDATE' is not a REST API method."
            },
            {
                "question": "What is a tier in software architecture?",
                "choices": [
                    {"description": "A type of database", "is_correct": False},
                    {"description": "A logical organization of the code",
                        "is_correct": False},
                    {"description": "A physical separation of components \
                     in an app",
                     "is_correct": True},
                    {"description": "A type of web server", "is_correct":
                     False}
                ],
                "feedback": "A tier in software architecture refers to \
                    a physical separation of components in an app."
            },
            {
                "question": "Which of the statements is false about a \
                    single-tier app?",
                "choices": [
                    {"description": "There is no network latency",
                     "is_correct": False},
                    {"description": "There is more data privacy and \
                     safety for the user.",
                     "is_correct": False},
                    {"description": "The publisher has complete control \
                     of the app after released",
                     "is_correct": True},
                    {"description": "The code is vulnerable to being tweaked \
                     or reverse engineered",
                     "is_correct": False}
                ],
                "feedback": "The statement 'The publisher has complete \
                    control of the app after released' is false about a \
                        single-tier app."
            },
            {
                "question": "What is a cache in software architecture?",
                "choices": [
                    {"description": "A high-speed memory used to store \
                     frequently accessed data",
                     "is_correct": True},
                    {"description": "A file system used to store large \
                     amounts of data",
                     "is_correct": False},
                    {"description": "A database used to store user \
                     information",
                     "is_correct": False},
                    {"description": "A programming language used to build \
                     applications",
                     "is_correct": False}
                ],
                "feedback": "A cache in software architecture is a \
                    high-speed memory used to store frequently accessed data."
            },
            {
                "question": "What is a cache miss?",
                "choices": [
                    {"description": "When data is successfully retrieved \
                     from the cache",
                     "is_correct": False},
                    {"description": "When the cache is full and data cannot \
                     be stored",
                     "is_correct": False},
                    {"description": "When the cache is cleared of all data",
                        "is_correct": False},
                    {"description": "When data is unsuccessfully retrieved \
                     from the cache and has to be fetched from the DB",
                     "is_correct": True}
                ],
                "feedback": "A cache miss occurs when data is unsuccessfully \
                    retrieved from the cache and has to be fetched from \
                        the database (DB)."
            },
            {
                "question": "Which pattern is commonly used to separate \
                    the presentation layer from the domain layer in a \
                        software application?",
                "choices": [
                    {"description": "Repository pattern", "is_correct": False},
                    {"description": "Model-view-controller (MVC) pattern",
                     "is_correct": True},
                    {"description": "Factory pattern", "is_correct": False},
                    {"description": "Observer pattern", "is_correct": False}
                ],
                "feedback": "The Model-view-controller (MVC) pattern is \
                    commonly used to separate the presentation layer from \
                        the domain layer in a software application."
            },
            {
                "question": "Which pattern is commonly used to ensure that \
                    only one instance of a class is created in a program?",
                "choices": [
                    {"description": "Strategy pattern", "is_correct": False},
                    {"description": "Singleton pattern", "is_correct": True},
                    {"description": "Facade pattern", "is_correct": False},
                    {"description": "Decorator pattern", "is_correct": False}
                ],
                "feedback": "The Singleton pattern is commonly used to \
                    ensure that only one instance of a class is created \
                        in a program."
            },
            {
                "question": "Which pattern is commonly used to add \
                    additional behavior or responsibilities to an object \
                        dynamically, without modifying its existing \
                            structure?",
                "choices": [
                    {"description": "Adapter pattern", "is_correct": False},
                    {"description": "Observer pattern", "is_correct": False},
                    {"description": "Facade pattern", "is_correct": False},
                    {"description": "Decorator pattern", "is_correct": True}
                ],
                "feedback": "The Decorator pattern is commonly used to \
                    add additional behavior or responsibilities to an object \
                        dynamically, without modifying its existing structure."
            },
            {
                "question": "Which pattern is commonly used to allow \
                    incompatible interfaces to work together by providing \
                        a common interface that both can adapt to?",
                "choices": [
                    {"description": "Chain of Responsibility pattern",
                        "is_correct": False},
                    {"description": "Strategy pattern", "is_correct": False},
                    {"description": "Facade pattern", "is_correct": False},
                    {"description": "Adapter pattern", "is_correct": True}
                ],
                "feedback": "The Adapter pattern is commonly used to allow \
                    incompatible interfaces to work together by providing a \
                        common interface that both can adapt to."
            },
            {
                "question": "Which pattern is commonly used to separate the \
                    construction of a complex object from its representation \
                        so that the same construction process can create \
                            different representations?",
                "choices": [
                    {"description": "Abstract Factory pattern", "is_correct":
                     True},
                    {"description": "Singleton pattern", "is_correct": False},
                    {"description": "Decorator pattern", "is_correct": False},
                    {"description": "Builder pattern", "is_correct": False}
                ],
                "feedback": "The Abstract Factory pattern is commonly used to \
                    separate the construction of a complex object from its \
                        representation so that the same construction process \
                            can create different representations."
            },
            {
                "question": "Which of the following is a potential \
                    disadvantage of serverless applications?",
                "choices": [
                    {"description": "Lost of control over infrastructure \
                     management",
                     "is_correct": True},
                    {"description": "Inability to scale automatically",
                        "is_correct": False},
                    {"description": "Inability to handle large data volumes",
                        "is_correct": False},
                    {"description": "Longer development time", "is_correct":
                     False}
                ],
                "feedback": "One potential disadvantage of serverless \
                    applications is the loss of control over infrastructure \
                        management."
            },
            {
                "question": "Which of the following is not a serverless \
                    database service offered by AWS?",
                "choices": [
                    {"description": "Aurora Serverless", "is_correct": False},
                    {"description": "DynamoDB", "is_correct": False},
                    {"description": "Neptune", "is_correct": False},
                    {"description": "ElasticSearch", "is_correct": True}
                ],
                "feedback": "ElasticSearch is not a serverless database \
                    service offered by AWS."
            },
            {
                "question": "What type of testing focuses on verifying the \
                    behavior of a small piece of code in isolation?",
                "choices": [
                    {"description": "Integration testing",
                     "is_correct": False},
                    {"description": "Acceptance testing", "is_correct": False},
                    {"description": "System testing", "is_correct": False},
                    {"description": "Unit testing", "is_correct": True}
                ],
                "feedback": "Unit testing focuses on verifying the behavior \
                    of a small piece of code in isolation."
            },
            {
                "question": "The following are some of the most popular test \
                    runners for unit testing in Python, except:",
                "choices": [
                    {"description": "unittest", "is_correct": False},
                    {"description": "nose or nose2", "is_correct": False},
                    {"description": "pytest", "is_correct": False},
                    {"description": "unitpytest", "is_correct": True}
                ],
                "feedback": "\"unitpytest\" is not a valid test runner for \
                    unit testing in Python. The correct options \
                        are \"unittest,\" \"nose or nose2,\" and \"pytest.\""
            },
            {
                "question": "What is the primary purpose of load testing?",
                "choices": [
                    {"description": "To verify the functionality of a \
                     software system",
                     "is_correct": False},
                    {"description": "To identify defects in a software system",
                        "is_correct": False},
                    {"description": "To measure the performance of a \
                     software system under a specific workload",
                     "is_correct": True},
                    {"description": "To ensure the security of a software \
                     system",
                        "is_correct": False}
                ],
                "feedback": "The primary purpose of load testing is to \
                    measure the performance of a software system under \
                        a specific workload."
            },
            {
                "question": "What is the term used to describe the delay \
                    or lag that occurs between sending a request and \
                        receiving a response in a software system?",
                "choices": [
                    {"description": "Bandwidth", "is_correct": False},
                    {"description": "Throughput", "is_correct": False},
                    {"description": "Latency", "is_correct": True},
                    {"description": "Jitter", "is_correct": False}
                ],
                "feedback": "Latency is the term used to describe the delay \
                    or lag that occurs between sending a request and \
                        receiving a response in a software system."
            },
            {
                "question": "What is the term used to describe the amount \
                    of work that a software system can perform in a given \
                        period of time?",
                "choices": [
                    {"description": "Throughput", "is_correct": True},
                    {"description": "Latency", "is_correct": False},
                    {"description": "Jitter", "is_correct": False},
                    {"description": "Bandwidth", "is_correct": False}
                ],
                "feedback": "Throughput is the term used to describe the \
                    amount of work that a software system can perform in \
                        a given period of time."
            }

        ]

        for data in question_data:
            question = Question(
                description=data["question"], feedback=data["feedback"])
            question.save()

            for choice in data["choices"]:
                answer = Answer(
                    description=choice["description"],
                    is_correct=choice["is_correct"])
                answer.save()
                question.answers.append(answer)
                question.save()

        return "Questions and choices created successfully!"
