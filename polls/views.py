"""
Module for render and response a request
"""

from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote

# Create your views here.


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

        question = self.get_object()

        if question.is_published():
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "Polls is unavailable right now")
            return HttpResponseRedirect(reverse("polls:index"), request)

    def get_context_data(self, **kwargs):
        # get the default context data
        context = super().get_context_data(**kwargs)
        # add extra field to the context
        context['can_vote'] = self.get_object().can_vote()
        print(context)
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
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )

    # Get current user
    this_user = request.user
    
    try:
        # Get vote from this user that vote to this question
        vote = this_user.vote_set.get(choice__question=question)
        
        # If user selected same choice, do nothing
        if vote.choice != selected_choice:
            
            # Otherwise change selected choice
            vote.choice = selected_choice
            vote.save()
            
    except Vote.DoesNotExist:    
        
        # If user hasn't vote yet just insert a new vote to model
        Vote.objects.create(user=this_user, choice=selected_choice)
    
    
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    messages.warning(request, "You haven't select a choice")
    return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))  # type: ignore
            )
