from math import e
import re
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from numpy import require

from .models import Question

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
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)