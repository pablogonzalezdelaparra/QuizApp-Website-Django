import unittest
from django.test import TestCase, Client
from django.urls import reverse
from quiz_app.models import Player, Question, Answer, Quiz
from quiz_app.views import QuizViews


class QuizViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_questions_view(self):
        response = self.client.get(reverse('questions_view'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

        # Simulate a POST request with selected answer
        question = Question(description='Test Question')
        question.save()
        answer = Answer(description='Test Answer', is_correct=True)
        answer.save()
        question.answers.append(answer)
        question.save()
        num_questions = 1
        username = 'Test User'
        response = self.client.post(reverse('index'), {
            'num_questions': num_questions,
            'username': username
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

        response = self.client.post(reverse('questions_view'), {
            'answer': answer.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz.html')

    def test_leaderboard_view(self):
        response = self.client.get(reverse('leaderboard_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard.html')


class QuestionModelTestCase(TestCase):
    def test_get_desc_correct_answer(self):
        question = Question(description='Test Question')
        question.save()
        correct_answer = Answer(description='Correct Answer', is_correct=True)
        correct_answer.save()
        incorrect_answer = Answer(
            description='Incorrect Answer', is_correct=False)
        incorrect_answer.save()
        question.answers.append(correct_answer)
        question.answers.append(incorrect_answer)
        question.save()

        self.assertEqual(question.get_id_correct_answer(), correct_answer.id)

    def test_get_id_correct_answer(self):
        question = Question(description='Test Question')
        question.save()
        correct_answer = Answer(description='Correct Answer', is_correct=True)
        correct_answer.save()
        incorrect_answer = Answer(description='Incorrect Answer',
                                  is_correct=False)
        incorrect_answer.save()
        question.answers.append(correct_answer)
        question.answers.append(incorrect_answer)
        question.save()

        self.assertEqual(str(question.get_id_correct_answer()),
                         str(correct_answer.id))


class PlayerModelTestCase(TestCase):
    def test_add_score(self):
        player = Player(username='Test User')
        player.save()
        player.add_score()
        self.assertEqual(player.score, 1)


class QuizModelTestCase(TestCase):
    def test_get_current_question(self):
        question1 = Question(description='Question 1')
        question1.save()
        question2 = Question(description='Question 2')
        question2.save()
        quiz = Quiz(questions=[question1, question2])
        quiz.save()
        current_question = quiz.get_current_question()
        self.assertEqual(current_question, question1)

    def test_answer_current_question_correct(self):
        question = Question(description='Test Question')
        question.save()
        correct_answer = Answer(description='Correct Answer', is_correct=True)
        correct_answer.save()
        incorrect_answer = Answer(description='Incorrect Answer',
                                  is_correct=False)
        incorrect_answer.save()
        question.answers.append(correct_answer)
        question.answers.append(incorrect_answer)
        question.save()
        quiz = Quiz(questions=[question])
        quiz.save()

        quiz.answer_current_question(correct_answer.id)
        self.assertEqual(quiz.score, 1)


if __name__ == '__main__':
    unittest.main()
