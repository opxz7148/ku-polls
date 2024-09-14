"""Module for render and response a request."""

import logging
from typing import Any
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed
)
from django.dispatch import receiver

from .models import Choice, Question, Vote

# Create your views here.

logger = logging.getLogger('polls')


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """Log to file when user login.

    Args:
        sender : Signal sender
        request (HttpRequest): Http request
        user (User): Authenticated user
    """
    ip = get_client_ip(request)

    logger.info(f'login user: {user} via ip: {ip}')


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """Log to file when user logout.

    Args:
        sender : Signal sender
        request (HttpRequest): Http request
        user (User): Authenticated user
    """
    ip = get_client_ip(request)

    logger.info(f'logout user: {user} via ip: {ip}')


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    """Log to file when user login failed.

    Args:
        sender : Signal sender
        credentials : User login attempt credentials.
    """
    logger.warning(f'login failed for: {credentials}')


class IndexView(generic.ListView):
    """Class responsible to show list of question."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")


class DetailView(generic.DetailView):
    """Class responsible to show detail of each question."""

    model = Question
    template_name = "polls/detail.html"

    def dispatch(self, request, *args, **kwargs):
        """Check does polls available or not before do anything else."""
        try:
            question = self.get_object()
        except Exception:
            messages.warning(request, "Polls is unavailable right now")
            return HttpResponseRedirect(reverse("polls:index"), request)

        if question.is_published():
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "Polls is unavailable right now")
            return HttpResponseRedirect(reverse("polls:index"), request)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Return a context data for passing into template.

        Returns:
            dict[str, Any]: Dict that map string with a context data
        """
        # Get original context
        context = super().get_context_data(**kwargs)

        # Get current user
        this_user = self.request.user

        # Get selected question
        question = self.get_object()

        if this_user.is_authenticated:
            try:
                # Try to got vote that got vote by this user
                previous_vote = this_user.vote_set.get(
                    user=this_user,
                    choice__question=question
                )
                context['previous_selected_id'] = previous_vote.choice.id
            except Vote.DoesNotExist:
                context["previous_selected_id"] = None

        return context


class ResultsView(generic.DetailView):
    """Class responsible to polls result."""

    model = Question
    template_name = "polls/results.html"

    def dispatch(self, request, *args, **kwargs):
        """Check does polls available or not before do anything else."""
        try:
            question = self.get_object()
        except Exception:
            messages.warning(request, "Polls is unavailable right now")
            return HttpResponseRedirect(reverse("polls:index"), request)

        if question.is_published():
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "Polls is unavailable right now")
            return HttpResponseRedirect(reverse("polls:index"), request)


@login_required
def vote(request, question_id):
    """Handle vote POST request by update polls result.

    Args:
        request (django.http.HttpRequest): http request from django
        question_id (int):  question id which is primary key of question
                            instance in database

    Returns:
        django.http.HttpResponse: http response with rendered content
    """
    if request.method == "GET":
        messages.warning(request, "Page unavailable")
        return HttpResponseRedirect(reverse("polls:index"), request)

    username = request.user.username

    # Check does question exist or not
    try:
        question = get_object_or_404(Question, pk=question_id)
        q_text = question.question_text
    except Question.DoesNotExist as err:

        logger.exception(f"Non-existent question {question_id} %s", err)

        messages.warning(request, "Polls does not exist")
        return HttpResponseRedirect(reverse("polls:index"), request)

    if not question.can_vote():
        messages.warning(request, "Polls is unavailable right now")
        return HttpResponseRedirect(reverse("polls:index"), request)

    try:
        selected_choice = question.choice_set.get(  # type: ignore
                pk=request.POST["choice"]
            )
        c_text = selected_choice.choice_text
    except KeyError as err:

        # Warn user if they doesn't select any choice
        messages.warning(request, "You haven't select the choice")

        # Log an exception
        logger.exception(f"User {username} doesn't select a choice %s", err)

        # Redirect user back to question detail with a message
        return HttpResponseRedirect(
            reverse("polls:detail", args=(question.id,))
        )

    except Choice.DoesNotExist as err:

        # Warn user if they select a choice from different polls
        messages.warning(request, "You have selected a invalid choice")

        # Log an exception
        logger.exception(f"User {username} select invalid choice %s", err)

        # Redirect user back to question detail with a message
        return HttpResponseRedirect(
            reverse("polls:detail", args=(question.id,))
        )

    # Get current user
    this_user = request.user

    try:
        # Get vote from this user that vote to this question
        vote = this_user.vote_set.get(choice__question=question)
        previous_choice = vote.choice.choice_text

        # If user selected same choice, do nothing
        if vote.choice != selected_choice:

            # Otherwise change selected choice
            vote.choice = selected_choice
            vote.save()

        # Log user vote
        log_string = "User {} change vote from {} to {} for question {}"
        logger.info(
            log_string.format(
                request.user.username,
                previous_choice,
                selected_choice.choice_text,
                question.question_text
                )
            )

        # Visual confirmation to user that their change already got recorded
        message_txt = "You have change your voted from {} to {}"
        messages.success(
            request,
            message_txt.format(previous_choice, selected_choice.choice_text)
        )

    except Vote.DoesNotExist as err:

        # If user hasn't vote yet just insert a new vote to model
        Vote.objects.create(user=this_user, choice=selected_choice)

        # Log user vote

        logger.exception(
            f"User {username} never vote for question {q_text} %s",
            err
            )
        logger.info(f"User {username} has vote {c_text} for question {q_text}")

        # Visual confirmation to user that their vote already got recorded
        messages.success(request, f"Your vote for {c_text} has been updated")

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))  # type: ignore
            )
