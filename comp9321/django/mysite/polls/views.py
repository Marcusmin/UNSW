from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from .models import Question
# Create your views here.

'''without html template
def index(request):
    latest = Question.objects.order_by('-pub_date')[:5]
    output = '! '.join([q.question_text for q in latest])
    return HttpResponse(output)
'''#with html template
def index(request):
    latest = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template("polls/index.html")
    context = {
        'latest':latest,
    }
    return HttpResponse(template.render(context, request))

def min(request):
    return HttpResponse("weijia_min")

def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("question does DoesNotExist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))