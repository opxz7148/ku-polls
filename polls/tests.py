"""
Polls app test file
"""

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question
# Create your tests here.


def create_question(
    question_text: str = "Test Question",
    pub_days: int = 0,
    end_days: int = None
) -> Question:

    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    pub_date = timezone.now() + datetime.timedelta(days=pub_days)

    if end_days is None:
        end_date = end_days
    else:
        end_date = timezone.now() + datetime.timedelta(days=end_days)

    return Question.objects.create(
        question_text=question_text,
        pub_date=pub_date,
        end_date=end_date
    )


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
