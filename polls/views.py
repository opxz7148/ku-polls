"""
Module for render and response a request
"""
import logging
from typing import Any
from django.db.models import F
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .models import Choice, Question, Vote

# Create your views here.

logger = logging.getLogger('polls')

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):    
    ip = request.META.get('REMOTE_ADDR')

    logger.info(f'login user: {user} via ip: {ip}')
    
@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs): 
    ip = request.META.get('REMOTE_ADDR')

    logger.info(f'logout user: {user} via ip: {ip}')


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    logger.warning(f'login failed for: {credentials}')


class IndexView(generic.ListView):
    """
    Class responsible to show list of question
    """

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")


class DetailView(generic.DetailView):
    """
    Class responsible to show detail of each question
    """
    model = Question
    template_name = "polls/detail.html"

    def dispatch(self, request, *args, **kwargs):
        
        try: 
            question = self.get_object()
        except:
            messages.warning(request, "Polls is unavailable right now")
            return HttpResponseRedirect(reverse("polls:index"), request)


        if question.is_published():
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "Polls is unavailable right now")
            return HttpResponseRedirect(reverse("polls:index"), request)
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
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
    """
    Class responsible to polls result
    """
    model = Question
    template_name = "polls/results.html"

    def dispatch(self, request, *args, **kwargs):

        question = self.get_object()

        if question.is_published():
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "Polls is unavailable right now")
            return HttpResponseRedirect(reverse("polls:index"), request)

@login_required
def vote(request, question_id):
    """ Function responsible to update number of vote after user has voted

    Args:
        request (django.http.HttpRequest): http request from django
        question_id (int):  question id which is primary key of question
                            instance in database

    Returns:
        django.http.HttpResponse: http response with rendered content
    """
    question = get_object_or_404(Question, pk=question_id)

    if not question.is_published():
        messages.warning(request, "Polls is unavailable right now")
        return HttpResponseRedirect(reverse("polls:index"), request)

    try:
        selected_choice = question.choice_set.get(  # type: ignore
                pk=request.POST["choice"]
            )

    except (KeyError, Choice.DoesNotExist):
    
        # Warn user if they doesn't select any choice
        messages.warning(request, "You haven't select the choice")
        
        # Redirect user back to question detail with a message 
        return HttpResponseRedirect(
            reverse("polls:detail", args=(question.id,))
        )

    # Get current user
    this_user = request.user
    
    try:
        # Get vote from this user that vote to this question
        vote = this_user.vote_set.get(choice__question=question)
        
        # If user selected same choice, do nothing
        if vote.choice != selected_choice:
            
            previous_choice = vote.choice.choice_text
            
            # Otherwise change selected choice
            vote.choice = selected_choice
            vote.save()
            
            # Visual confirmation to user that their change already got recorded
            messages.success(request, f"You have change your voted from {previous_choice} to {selected_choice.choice_text}")
            
    except Vote.DoesNotExist:    
        
        # If user hasn't vote yet just insert a new vote to model
        Vote.objects.create(user=this_user, choice=selected_choice)
        
        # Visual confirmation to user that their vote already got recorded
        messages.success(request, f"Your vote for {selected_choice.choice_text} has been updated")
    
    
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))  # type: ignore
            )
