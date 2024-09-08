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

def create_dummies_question_and_2_choice(
    question_text: str = "Test question",
    pub_days: int = 0,
    end_days: int = None
) -> tuple[Question, Choice, Choice]:
    """
    Create a dummies question with 2 associates choice

    Args:
        question_text (str, optional): Question text. Defaults to "Test question".
        pub_days (int, optional): Number of day until question publish. Defaults to 0.
        end_days (int, optional): Number of day until question end. Defaults to None.

    Returns: tuple of question and it 2 choice in order
        Question, Choice, Choice
    """
    q = create_question(question_text, pub_days, end_days)
    c1 = q.choice_set.create(choice_text="choice1")
    c2 = q.choice_set.create(choice_text="choice2")
    
    return q, c1, c2
        
def create_user(username="tester", password="hackmepls") -> User:
    """Create tester user where their name is tester and hackmepls as a password

    Args:
        username (str, optional): Defaults to "tester".
        password (str, optional): Defaults to "hackmepls".
    return:
        User : User object
    """
    return User.objects.create(username=username, password=password)
    
def user_vote(client: Client, choice: Choice) -> HttpResponse:
    """
    Make user vote to certain choice

    Args:
        user (User): User that going to vote
        choice (Choice): Choice that user going to vote for

    """
    url = reverse("polls:vote", args=(choice.question.id,))
        
    response = client.post(url, {"choice": choice.id})
    
    return response