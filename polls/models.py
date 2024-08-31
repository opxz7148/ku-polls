"""
File for create database model 
"""

import datetime
from turtle import mode

from django.db import models
from django.utils import timezone
# Create your models here.


class Question(models.Model):
    """
    Question model
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.datetime.now)
    end_date = models.DateTimeField("polls end date", default=None, blank=True, null=True)

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


class Choice(models.Model):
    """
    Question Choice model
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.choice_text)
