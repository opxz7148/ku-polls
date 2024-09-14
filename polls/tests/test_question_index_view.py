"""
Polls app test file
"""

import datetime

from django.test import TestCase
from django.urls import reverse

from .helper import *


class QuestionIndexViewTests(TestCase):
    """
    Test case for index view
    """
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", pub_days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on the
        index page.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(
            question_text="Past question 1.", pub_days=-30
        )
        question2 = create_question(
            question_text="Past question 2.", pub_days=-5
        )
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

    def test_both_past_and_future(self):
        """
        The question index page must display only published question.
        """
        # Create question both in the future and in the past
        past_question1 = create_question("Past question", pub_days=-5)
        past_question2 = create_question("Past question2", pub_days=-10)
        _ = create_question("Future question2", pub_days=5)

        # Get a response from view
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

    def test_past_poll_that_ended_and_not(self):
        """
        The question index page must display only published question.
        """
        # Create question that published in the past
        # that already ended and not yet
        past_question_ended = create_question(
            "Past question", pub_days=-5, end_days=-2
        )
        past_question_not_ended = create_question(
            "Past question2", pub_days=-5, end_days=5
        )

        # Get a response from view
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past_question_not_ended, past_question_ended]
        )

    def test_future_poll_that_ended_and_not(self):
        """
        The question index page must display only published question.
        """
        # Create question that published in the future that already ended and not yet
        future_question_ended = create_question("Past question", pub_days=5, end_days=-2)
        future_question_not_ended = create_question("Past question2", pub_days=5, end_days=6)

        # Get a response from view
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            []
        )
