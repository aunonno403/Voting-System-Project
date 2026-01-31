from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Choice, Vote

# Get questions and display those questions
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    # If user is logged in, get their votes
    user_votes = {}
    if request.user.is_authenticated:
        votes = Vote.objects.filter(user=request.user, question__in=latest_question_list)
        user_votes = {vote.question_id: vote.choice_id for vote in votes}
    
    context = {
        'latest_question_list': latest_question_list,
        'user_votes': user_votes,
    }
    return render(request, 'polls/index.html', context)

# Show question and choices
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    # Check if user already voted
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(user=request.user, question=question)
        except Vote.DoesNotExist:
            pass
    
    context = {
        'question': question,
        'user_vote': user_vote,
    }
    return render(request, 'polls/detail.html', context)

#Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    
    # Check if user voted
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(user=request.user, question=question)
        except Vote.DoesNotExist:
            pass
    
    context = {
        'question': question,
        'user_vote': user_vote,
    }
    return render(request, 'polls/results.html', context)

# Vote for a question choice
@login_required(login_url='accounts:login')
def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', 
                      { 'question': question,
                        'error_message': 'You did not select a choice.'})
    
    # Check if user already voted on this question
    existing_vote = Vote.objects.filter(user=request.user, question=question).first()
    
    if existing_vote:
        # Update existing vote
        old_choice = existing_vote.choice
        old_choice.votes -= 1
        old_choice.save()
        
        existing_vote.choice = selected_choice
        existing_vote.save()
        
        selected_choice.votes += 1
        selected_choice.save()
        
        messages.success(request, 'Your vote has been updated!')
    else:
        # Create new vote
        Vote.objects.create(
            user=request.user,
            choice=selected_choice,
            question=question
        )
        selected_choice.votes += 1
        selected_choice.save()
        
        messages.success(request, 'Your vote has been recorded!')
    
    return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))
    