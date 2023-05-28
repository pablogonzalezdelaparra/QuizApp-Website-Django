"""
import unittest
from django.test import Client, RequestFactory, TestCase
from quiz_app.models import Player, Question, Answer
from django.test import TestCase, Client
from django.urls import reverse
from quiz_app.models import Player, Question, Answer, Quiz
from quiz_app.views import QuizViews


class QuizViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Other setup steps, if any

    def test_index_view_get(self):
        response = self.client.get('/')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions for the index view
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_post(self):
        data = {
            'num_questions': 5,
            'username': 'JohnDoe'
        }
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/quiz/')

    def test_questions_view_get(self):
        response = self.client.get('/quiz/')

    def test_leaderboard_view(self):
        response = self.client.get(reverse('leaderboard_view'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions for the questions view GET request
        self.assertTemplateUsed(response, 'leaderboard.html')

    def test_questions_view_post_correct_answer(self):
        # Create a question
        question = Question(description='Sample question')
        question.save()

        # Create a correct answer for the question
        correct_answer = Answer(description='Correct answer', is_correct=True)

    def test_reset_quiz(self):
        # Create a mock player
        player = Player(username='Test Player')
        player.save()

        # Set the player_id in the session
        self.client.session['player_id'] = str(player.id)
        self.client.session.save()

        # Make a GET request to reset the quiz
        response = self.client.get(reverse('reset_quiz'))

        # Assert the response
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('index'))

        # Assert that the session data is cleared
        self.assertNotIn('question_number', self.client.session)
        self.assertNotIn('player_id', self.client.session)
        self.assertNotIn('random_questions', self.client.session)


class QuestionModelTestCase(TestCase):
    def test_questions_view_post_incorrect_answer(self):
        # Create a mock question and answer
        question = Question(description="What is the capital of France?")

    def test_leaderboard_view(self):
        response = self.client.get('/leaderboard/')
        self.assertEqual(response.status_code, 200)
        # Add more assertions for the leaderboard view

    def test_check_answer_with_correct_answer(self):
        # Create a player
        player = Player(username='Test Player')
        player.save()

        # Create a mock question
        question = Question(description='Test Question')
        question.save()

        # Create a correct answer for the question
        correct_answer = Answer(description='Correct Answer', is_correct=True)
        correct_answer.save()
        question.answers.append(correct_answer)
        question.save()

        # Set up session data
        session = self.client.session
        session['question_number'] = 1
        session['random_questions'] = [str(question.id)]
        session['player_id'] = str(player.id)
        session.save()

        # print("id", correct_answer.id)

        # Submit the form with the correct answer
        data = {'answer': str(correct_answer.id), 'feedback': 'Correct!'}
        response = self.client.post('/quiz/', data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Correct!')

    def test_check_answer_with_incorrect_answer(self):
        # Create a player
        player = Player(username='Test Player')
        player.save()
        # Create a mock question
        question = Question(description='Test Question')
        question.save()

        # Create an incorrect answer for the question
        incorrect_answer = Answer(description='Incorrect Answer',
                                  is_correct=False)
        incorrect_answer.save()
        question.answers.append(incorrect_answer)
        question.save()

        # Set up session data
        session = self.client.session
        session['question_number'] = 1
        session['random_questions'] = [str(question.id)]
        session['player_id'] = str(player.id)

        session.save()

        # Submit the form with the incorrect answer
        data = {'answer': str(incorrect_answer.id), 'feedback': 'Incorrect!'}
        response = self.client.post('/quiz/', data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Incorrect.')


class PlayerModelTestCase(TestCase):
    # Existing test methods

    def test_get_score_with_valid_player_id(self):
        # Create a mock player with a score of 5
        player = Player(username='Test Player', score=5)
        player.save()

        # Set the player_id in the session
        self.client.session['player_id'] = str(player.id)
        self.client.session.save()

        # Make a GET request to get the player's score
        response = self.client.get(reverse('leaderboard_view'))

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '5')


if __name__ == '__main__':
    unittest.main()
"""
