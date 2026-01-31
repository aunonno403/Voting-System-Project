from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pollApp.models import Question, Choice


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('polls:index')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('polls:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'polls:index')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('index')


@login_required
def profile(request):
    """User profile showing voting history"""
    user = request.user
    
    # Get all votes by this user
    user_votes = Choice.objects.filter(vote__user=user).select_related('question')
    
    # Get questions the user voted on
    voted_questions = Question.objects.filter(
        choice__vote__user=user
    ).distinct().order_by('-pub_date')
    
    context = {
        'user': user,
        'voted_questions': voted_questions,
        'total_votes': user_votes.count(),
    }
    
    return render(request, 'accounts/profile.html', context)
