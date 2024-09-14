"""
Polls app test file
"""

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import Client

from polls.models import Question, Choice, Vote
from .helper import *


class QuestionResultViewTests(TestCase):
    """
    Test case for question detail view
    """
    def test_visitor_able_to_see_polls_result(self):
        """Visitor must able to see polls result"""
        q, _, _ = create_dummies_question_and_2_choice()
        
        url = reverse("polls:results", args=(q.id, ))
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
    def test_user_able_to_see_polls_result(self):
        """User must able to see polls result"""
        q, _, _ = create_dummies_question_and_2_choice()
        
        user = create_test_user()
        self.client.force_login(user)
        
        url = reverse("polls:results", args=(q.id, ))
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
    def test_user_redirect_from_unavailable_polls_result(self):
        """User must redirect to index page when reach unavailable polls result"""
        user = create_test_user()
        self.client.force_login(user)
        
        url = reverse("polls:results", args=(100, ))
        
        response = self.client.get(url)
        
        self.assertRedirects(
            response,
            expected_url="/polls/"
            )
    
    def test_visitor_redirect_from_unavailable_polls_result(self):
        """Visitor must redirect to index page when reach unavailable polls result"""
        
        url = reverse("polls:results", args=(100, ))
        
        response = self.client.get(url)
        
        self.assertRedirects(
            response,
            expected_url="/polls/"
            )