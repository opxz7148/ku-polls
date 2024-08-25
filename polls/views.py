from math import e

from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse

from .models import Choice, Question

# Create your views here.

def index(request):
    
    # Query list of question from DB
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    
    # Create a context for template
    context = {
        "latest_question_list": latest_question_list
    }
    
    # Render a template then return to response the request
    return render(request, "polls/index.html", context)
    
def detail(request, question_id):

    # Get a question from database or raise 404 if object not found
    question = get_object_or_404(Question, pk=question_id)
    
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) # type: ignore
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
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,))) # type: ignore