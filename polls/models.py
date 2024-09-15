"""File for create database model."""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    """Question model."""

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
        """Return question text."""
        return str(self.question_text)

    def was_published_recently(self) -> bool:
        """
        Return boolean values which indicate does question was publish in 1 days or not.

        Returns:
            bool:
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self) -> bool:
        """Return a boolean vales which tell that does question is published or not.

        Returns:
            bool:   True if current time is already pass question
                    published date. Otherwise return False
        """
        now = timezone.now()
        return now >= self.pub_date

    def is_end(self) -> bool:
        """Return a boolean vales which tell that does question is ended or not.

        Returns:
            bool:   False if current time is already pass question end date.
                    Otherwise return True
        """
        if self.end_date is None:
            return False

        now = timezone.now()
        return now > self.end_date

    def can_vote(self) -> bool:
        """Return a boolean vales which tell that does question is voteable or not.

        Returns:
            bool: True if able to vote this question, return False otherwise
        """
        return self.is_published() and (not self.is_end())

    @property
    def has_end_date(self):
        """Return a boolean vales which tell that does question has ended or not."""
        if self.end_date is None:
            return False
        return True

    @property
    def available(self) -> bool:
        """Return a boolean vales which tell that does question is available or not."""
        return self.can_vote()


class Choice(models.Model):
    """Question Choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    @property
    def votes(self) -> int:
        """Return number of votes on this choice."""
        return self.vote_set.count()

    def __str__(self) -> str:
        """Return choice text."""
        return str(self.choice_text)


class Vote(models.Model):
    """A vote by user."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return choice test."""
        return self.choice_text
