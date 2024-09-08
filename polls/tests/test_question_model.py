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


class QuestionModelTests(TestCase):
    """
    Test case for Question model.
    """

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(
                hours=23,
                minutes=59,
                seconds=59
            )
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_past_pub_date(self):
        """
        Is published must return true if publish date is in the past
        """

        # Create question with published day is in the past
        q = create_question(pub_days=-1)
        self.assertTrue(q.is_published())

    def test_is_published_with_future_pub_date(self):
        """
        Is published must return false if publish date is in the future
        """

        # Create question with published day is in the past
        q = create_question(pub_days=1)
        self.assertFalse(q.is_published())

    def test_is_published_with_today_pub_date(self):
        """
        Is published must return True if publish date is today
        """

        # Create question with published day is today
        q = create_question()
        self.assertTrue(q.is_published())

    def test_is_end_with_past_end_date(self):
        """
        is_end must return True if end date is in the past
        """

        # Create question with end day is today
        q = create_question(end_days=-1)
        self.assertTrue(q.is_end())

    def test_is_end_with_future_end_date(self):
        """
        is_end must return False if end date is in the future
        """

        # Create question with end day is in the future
        q = create_question(end_days=1)
        self.assertFalse(q.is_end())

    def test_is_end_with_today_end_date(self):
        """
        is_end must return True if end date is today
        """

        # Create question with end day is today
        q = create_question(end_days=0)
        self.assertTrue(q.is_end())

    def test_can_vote_with_pub_date_in_the_past_without_end_date(self):
        """
        can_vote must return True when their are
        no end_date and pub_date in the past
        """
        q = create_question(pub_days=-1)
        self.assertTrue(q.can_vote())

    def test_can_vote_with_pub_date_in_the_future_without_end_date(self):
        """
        can_vote must return False when their are
        no end_date and pub_date in the past
        """
        q = create_question(pub_days=1)
        self.assertFalse(q.can_vote())

    def test_can_vote_with_pub_date_is_today_without_end_date(self):
        """
        can_vote must return True when their are
        no end_date and pub_date is today
        """
        q = create_question()
        self.assertTrue(q.can_vote())

    def test_can_vote_with_pub_date_and_end_date_in_the_future(self):
        """
        can_vote must return False when their are end_date and pub_date in the future
        """
        q = create_question(pub_days=1, end_days=2)
        self.assertFalse(q.can_vote())

    def test_can_vote_with_pub_date_and_end_date_in_the_past(self):
        """
        can_vote must return False when their are
        end_date and pub_date in the past
        """
        q = create_question(pub_days=-2, end_days=-1)
        self.assertFalse(q.can_vote())

    def test_can_vote_with_pub_date_in_the_past_and_end_date_in_the_future(self):
        """
        can_vote must return True when their are
        end_date in the future and pub_date in the past
        """
        q = create_question(pub_days=-2, end_days=2)
        self.assertTrue(q.can_vote())

    def test_can_vote_with_pub_date_in_the_future_and_end_date_in_the_past(self):
        """
        can_vote must return False when their are
        end_date in the past and pub_date in the future
        """
        q = create_question(pub_days=2, end_days=-2)
        self.assertFalse(q.can_vote())

    def test_can_vote_with_pub_date_and_end_date_is_today(self):
        """
        can_vote must return True when their are end_date and pub_date is today
        """
        q = create_question(pub_days=0, end_days=0)
        self.assertFalse(q.can_vote())
