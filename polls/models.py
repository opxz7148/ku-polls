"""File for create database model"""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    """Question model"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(
        "date published",
        default=timezone.datetime.now
        )
    end_date = models.DateTimeField(
        "polls end date",
        default=None,
        blank=True,
        null=True
        )

    def __str__(self) -> str:
        return str(self.question_text)

    def was_published_recently(self) -> bool:
        """Function to tell that does certain question are
           recently publish or not

        Returns:
            bool:
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self) -> bool:
        """Function to tell whether poll are already published or not.

        Returns:
            bool:   True if current time is already pass question
                    published date. Otherwise return False
        """

        now = timezone.now()
        return now >= self.pub_date

    def is_end(self) -> bool:
        """Function to tell whether poll are already past end date or not.

        Returns:
            bool:   False if current time is already pass question end date.
                    Otherwise return True
        """
        if self.end_date is None:
            return False

        now = timezone.now()
        return now > self.end_date

    def can_vote(self) -> bool:
        """Function to tell whether this question is available to vote or not.

        Returns:
            bool: True if able to vote this question, return False otherwise
        """

        return self.is_published() and (not self.is_end())

    @property
    def has_end_date(self):
        if self.end_date is None:
            return False
        return True

    @property
    def available(self) -> bool:
        return self.can_vote()


class Choice(models.Model):
    """Question Choice model."""
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    @property
    def votes(self) -> int:
        return self.vote_set.count()

    def __str__(self) -> str:
        return str(self.choice_text)


class Vote(models.Model):
    """A vote by user."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.choice_text
