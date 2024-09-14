"""
Polls app test file
"""

import datetime

from django.test import TestCase
from django.urls import reverse

from .helper import *


class QuestionDetailViewTests(TestCase):
    """
    Test case for question detail view
    """
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(
                question_text="Future question.",
                pub_days=5
            )
        url = reverse(
                "polls:detail",
                args=(future_question.id,)  # type: ignore
            )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
                question_text="Past Question.",
                pub_days=-5
            )
        url = reverse("polls:detail", args=(past_question.id,))  # type: ignore
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_authorized_user_must_able_to_visit_question_that_they_have_not_vote_yet(self):
        
        question, _, _ = create_dummies_question_and_2_choice()
        user = create_test_user()
        
        self.client.force_login(user)
        
        res = self.client.get(reverse("polls:detail", args=(question.id,)))
        
        self.assertEqual(res.status_code, 200)
        
    def test_user_prev_choice_must_got_preselected(self):
        
        question, c1, _ = create_dummies_question_and_2_choice()
        user = create_test_user()
        
        self.client.force_login(user)
        
        user_vote(self.client, c1)
        
        res = self.client.get(reverse("polls:detail", args=(question.id,)))
        
        self.assertContains(res, f'value="{c1.id}" checked')
