# Quiz App

The Quiz App is a web application that allows users to participate in quizzes by answering questions and keeping track of their scores. Users can also view the leaderboard to see the top scorers.

## Web Location

Please note that the Quiz App is also hosted and accessible at https://www.quizapp.com.

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/quiz-app.git
```

2. Navigate to the project directory:

```
cd quiz-app
```

3. Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

4. Install the required dependencies:

```
pip install -r requirements.txt
```

5. Run the database migrations:

```
python manage.py migrate
```

6. Start the development server:

```
python manage.py runserver
```

7. Access the application at [http://localhost:8000](http://localhost:8000).

## Routes

- **Index**: `/` (GET)
  - Displays the index page where users can enter the number of questions and their username to start the quiz.

- **Quiz**: `/quiz/` (GET, POST)
  - Displays a question and its answers. If the user submits an answer, it checks if it's correct and displays feedback. If there are more questions, it proceeds to the next question. Otherwise, it shows the final score.

- **Leaderboard**: `/leaderboard/` (GET)
  - Displays the leaderboard, showing the top 10 players ordered by score and upload date.

- **Reset Quiz**: `/reset_quiz/` (GET)
  - Resets the quiz by clearing the session data and redirects to the index page.

## Models

- **Player**
  - Represents a player with a username and score.

- **Question**
  - Represents a question with a description and a list of associated answers.

- **Answer**
  - Represents an answer with a description and a flag indicating if it's correct.

## Additional Information

- The project uses Django as the web framework and MongoEngine as the object-document mapper (ODM) for MongoDB.
- The `QuizViews` class in `views.py` contains the main logic for handling requests and rendering templates.
- The project includes templates in the `templates` directory and static files in the `static` directory.
- The application uses session data to store the state of the quiz (e.g., current question, player ID).
- The leaderboard displays the top 10 players based on their scores and upload dates. Ties are handled by assigning ranks.
- The project includes a management command `create_question` that creates a mock question with answers and saves it to the database.

Feel free to modify and extend the project as per your requirements.

## License

This project is licensed under the [MIT License](LICENSE).