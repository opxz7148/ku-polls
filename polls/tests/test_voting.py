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


class VotingTest(TestCase):
    """
    Test voting behavior
    """
    
    def test_only_authorized_user_can_vote(self):
        
        dummies_question, dummies_choice1, _ = create_dummies_question_and_2_choice()
        
        # url = reverse("polls:vote", args=(dummies_question.id,))
        
        # response = self.client.post(url, {"choice": dummies_choice1.id})
        
        response = user_vote(self.client, dummies_choice1)
                
        self.assertRedirects(
            response,
            expected_url=f"/accounts/login/?next=/polls/{dummies_question.id}/vote/"
        )
        
    def test_authorized_user_can_vote(self):
        """
        Authorized user should be able to voted and vote result should be updated
        """
        user = create_test_user()
        self.client.force_login(user)
        
        _, dummies_choice1, _ = create_dummies_question_and_2_choice()
        
        prev_vote_count = dummies_choice1.vote_set.count()
                
        user_vote(self.client, dummies_choice1)
        
        new_vote_count = dummies_choice1.vote_set.count()

        self.assertEqual(prev_vote_count + 1, new_vote_count)        
        
    def test_authorized_user_can_change_vote(self):
        """
        Authorized user should be able to change their voted and vote result should be updated
        """
        
        user = create_test_user()
        self.client.force_login(user)
        
        _, dummies_choice1, dummies_choice2 = create_dummies_question_and_2_choice()
        
        user_vote(self.client, dummies_choice1)
        
        self.assertEqual(dummies_choice1.vote_set.count(), 1)
        self.assertEqual(dummies_choice2.vote_set.count(), 0)
        
        user_vote(self.client, dummies_choice2)
        
        self.assertEqual(dummies_choice1.vote_set.count(), 0)
        self.assertEqual(dummies_choice2.vote_set.count(), 1)
        
    def test_multiple_user_vote(self):
        """
        Test case where multiple user has login and vote on the same polls and same question
        """
        
        user1 = create_test_user("tester1")
        user2 = create_test_user("tester2")
        
        _, dummies_choice1, dummies_choice2 = create_dummies_question_and_2_choice()
        
        self.client.force_login(user1)
        user_vote(self.client, dummies_choice1)
        
        self.assertEqual(dummies_choice1.vote_set.count(), 1)
        self.assertEqual(dummies_choice2.vote_set.count(), 0)
        
        self.client.logout
        
        self.client.force_login(user2)
        user_vote(self.client, dummies_choice1)
        
        self.assertEqual(dummies_choice1.vote_set.count(), 2)
        self.assertEqual(dummies_choice2.vote_set.count(), 0)
        
        user_vote(self.client, dummies_choice2)
        
        self.assertEqual(dummies_choice1.vote_set.count(), 1)
        self.assertEqual(dummies_choice2.vote_set.count(), 1)
        
        self.client.logout
        
        self.client.force_login(user1)
        user_vote(self.client, dummies_choice2)
        
        self.assertEqual(dummies_choice1.vote_set.count(), 0)
        self.assertEqual(dummies_choice2.vote_set.count(), 2)
        
    def test_user_vote_same_choice(self):
        """
        If user vote on same choice as previous vote, vote count must remain the same
        """
        user = create_test_user()
        self.client.force_login(user)
        
        _, c1, _ = create_dummies_question_and_2_choice()
        
        user_vote(self.client, c1)
        user_vote(self.client, c1)

        self.assertEqual(c1.vote_set.count(), 1)
    