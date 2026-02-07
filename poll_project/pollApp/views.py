from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Question, Choice, Vote, Category, Comment


def index(request):
    """List all active polls with filtering and search"""
    # Get active, non-draft polls
    polls = Question.objects.filter(is_draft=False)
    
    # Apply visibility filter
    if not request.user.is_authenticated:
        # Non-authenticated users can only see public polls
        polls = polls.filter(visibility='public')
    else:
        # Authenticated users can see:
        # - Public polls
        # - Password-protected polls (they'll need to enter password to vote)
        # - Their own private polls
        # - Private polls they're invited to
        polls = polls.filter(
            Q(visibility='public') | 
            Q(visibility='password') | 
            Q(visibility='private', created_by=request.user) |
            Q(visibility='private', invited_users=request.user)
        ).distinct()  # distinct() to avoid duplicates from invited_users
    
    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        polls = polls.filter(category__slug=category_slug)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        polls = polls.filter(
            Q(question_text__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by status
    status = request.GET.get('status', 'active')
    if status == 'active':
        # Only active polls
        polls = [p for p in polls if p.is_active()]
    elif status == 'upcoming':
        polls = [p for p in polls if p.is_upcoming()]
    elif status == 'expired':
        polls = [p for p in polls if p.is_expired()]
    elif status == 'all':
        polls = list(polls)
    else:
        polls = [p for p in polls if p.is_active()]
    
    # Get user votes if authenticated
    user_votes = {}
    if request.user.is_authenticated:
        votes = Vote.objects.filter(user=request.user)
        for vote in votes:
            if vote.question_id not in user_votes:
                user_votes[vote.question_id] = []
            user_votes[vote.question_id].append(vote.choice_id)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    context = {
        'polls': polls,
        'user_votes': user_votes,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
        'status': status,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """Show poll details and voting interface"""
    question = get_object_or_404(Question, pk=question_id)
    
    # Check if poll is draft
    if question.is_draft and (not request.user.is_authenticated or request.user != question.created_by):
        messages.error(request, 'This poll is not available.')
        return redirect('polls:index')
    
    # Check visibility
    if question.visibility == 'private':
        # Private polls only accessible by creator and invited users
        if not request.user.is_authenticated:
            messages.error(request, 'You do not have permission to view this poll.')
            return redirect('polls:index')
        
        is_creator = request.user == question.created_by
        is_invited = question.invited_users.filter(id=request.user.id).exists()
        
        if not (is_creator or is_invited):
            messages.error(request, 'You do not have permission to view this poll.')
            return redirect('polls:index')
    
    # Handle password-protected polls
    if question.visibility == 'password':
        if not request.session.get(f'poll_password_{question_id}'):
            # Check if password is being submitted
            if request.method == 'POST' and 'poll_password' in request.POST:
                entered_password = request.POST.get('poll_password')
                if entered_password == question.password:
                    request.session[f'poll_password_{question_id}'] = True
                else:
                    messages.error(request, 'Incorrect password.')
                    return render(request, 'polls/password.html', {'question': question})
            else:
                return render(request, 'polls/password.html', {'question': question})
    
    # Check if user already voted
    user_votes = []
    if request.user.is_authenticated:
        user_votes = Vote.objects.filter(user=request.user, question=question).values_list('choice_id', flat=True)
    
    # Get comments
    comments = question.comments.all()[:20]
    
    context = {
        'question': question,
        'user_votes': list(user_votes),
        'comments': comments,
    }
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    """Display poll results"""
    question = get_object_or_404(Question, pk=question_id)
    
    # Check visibility (same as detail)
    if question.is_draft and (not request.user.is_authenticated or request.user != question.created_by):
        messages.error(request, 'This poll is not available.')
        return redirect('polls:index')
    
    if question.visibility == 'private':
        # Private polls only accessible by creator and invited users
        if not request.user.is_authenticated:
            messages.error(request, 'You do not have permission to view this poll.')
            return redirect('polls:index')
        
        is_creator = request.user == question.created_by
        is_invited = question.invited_users.filter(id=request.user.id).exists()
        
        if not (is_creator or is_invited):
            messages.error(request, 'You do not have permission to view this poll.')
            return redirect('polls:index')
    
    # Handle password-protected polls
    if question.visibility == 'password':
        if not request.session.get(f'poll_password_{question_id}'):
            messages.warning(request, 'This poll is password protected. Please enter the password first.')
            return redirect('polls:detail', question_id=question_id)
    
    # Check if user voted
    user_votes = []
    if request.user.is_authenticated:
        user_votes = Vote.objects.filter(user=request.user, question=question)
    
    # Get comments
    comments = question.comments.all()[:20]
    
    context = {
        'question': question,
        'user_votes': user_votes,
        'comments': comments,
    }
    return render(request, 'polls/results.html', context)


@login_required(login_url='accounts:login')
def vote(request, question_id):
    """Handle voting with support for single and multiple choice"""
    question = get_object_or_404(Question, pk=question_id)
    
    # Check visibility and password protection
    if question.visibility == 'private':
        is_creator = request.user == question.created_by
        is_invited = question.invited_users.filter(id=request.user.id).exists()
        
        if not (is_creator or is_invited):
            messages.error(request, 'You do not have permission to vote on this poll.')
            return redirect('polls:index')
    
    if question.visibility == 'password':
        if not request.session.get(f'poll_password_{question_id}'):
            messages.warning(request, 'Please enter the password to access this poll.')
            return redirect('polls:detail', question_id=question_id)
    
    # Check if poll is active
    if not question.is_active():
        messages.error(request, 'This poll is not currently accepting votes.')
        return redirect('polls:results', question_id=question_id)
    
    if request.method != 'POST':
        return redirect('polls:detail', question_id=question_id)
    
    if question.allow_multiple_choices:
        # Multiple choice voting
        selected_choices = request.POST.getlist('choice')
        
        if not selected_choices:
            messages.error(request, 'You must select at least one choice.')
            return redirect('polls:detail', question_id=question_id)
        
        # Remove old votes for this question
        old_votes = Vote.objects.filter(user=request.user, question=question)
        for old_vote in old_votes:
            old_vote.choice.votes -= 1
            old_vote.choice.save()
        old_votes.delete()
        
        # Add new votes
        for choice_id in selected_choices:
            try:
                choice = question.choice_set.get(pk=choice_id)
                Vote.objects.create(user=request.user, choice=choice, question=question)
                choice.votes += 1
                choice.save()
            except Choice.DoesNotExist:
                continue
        
        messages.success(request, f'Your votes have been recorded! ({len(selected_choices)} choices)')
    
    else:
        # Single choice voting
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, 'You did not select a valid choice.')
            return redirect('polls:detail', question_id=question_id)
        
        # Check if user already voted
        existing_votes = Vote.objects.filter(user=request.user, question=question)
        
        if existing_votes.exists():
            # Update existing vote
            for old_vote in existing_votes:
                old_choice = old_vote.choice
                old_choice.votes -= 1
                old_choice.save()
                old_vote.delete()
            
            Vote.objects.create(user=request.user, choice=selected_choice, question=question)
            selected_choice.votes += 1
            selected_choice.save()
            
            messages.success(request, 'Your vote has been updated!')
        else:
            # Create new vote
            Vote.objects.create(user=request.user, choice=selected_choice, question=question)
            selected_choice.votes += 1
            selected_choice.save()
            
            messages.success(request, 'Your vote has been recorded!')
    
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


@login_required(login_url='accounts:login')
def add_comment(request, question_id):
    """Add a comment to a poll"""
    question = get_object_or_404(Question, pk=question_id)
    
    # Check visibility and password protection
    if question.visibility == 'private':
        is_creator = request.user == question.created_by
        is_invited = question.invited_users.filter(id=request.user.id).exists()
        
        if not (is_creator or is_invited):
            messages.error(request, 'You do not have permission to comment on this poll.')
            return redirect('polls:index')
    
    if question.visibility == 'password':
        if not request.session.get(f'poll_password_{question_id}'):
            messages.warning(request, 'Please enter the password to access this poll.')
            return redirect('polls:detail', question_id=question_id)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '').strip()
        
        if comment_text:
            Comment.objects.create(
                question=question,
                user=request.user,
                text=comment_text
            )
            messages.success(request, 'Your comment has been added!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect('polls:results', question_id=question_id)


@login_required(login_url='accounts:login')
def delete_comment(request, comment_id):
    """Delete a comment (only by owner)"""
    comment = get_object_or_404(Comment, pk=comment_id)
    question_id = comment.question.id
    
    if request.user == comment.user or request.user.is_staff:
        comment.delete()
        messages.success(request, 'Comment deleted.')
    else:
        messages.error(request, 'You can only delete your own comments.')
    
    return redirect('polls:results', question_id=question_id)


def category_polls(request, slug):
    """Show polls in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    polls = Question.objects.filter(category=category, is_draft=False)
    
    # Filter by visibility
    if not request.user.is_authenticated:
        polls = polls.filter(visibility='public')
    else:
        # Authenticated users can see public, password-protected, their own private polls, and polls they're invited to
        polls = polls.filter(
            Q(visibility='public') | 
            Q(visibility='password') | 
            Q(visibility='private', created_by=request.user) |
            Q(visibility='private', invited_users=request.user)
        ).distinct()
    
    # Only active polls
    polls = [p for p in polls if p.is_active()]
    
    # Get user votes
    user_votes = {}
    if request.user.is_authenticated:
        votes = Vote.objects.filter(user=request.user, question__in=[p.id for p in polls])
        for vote in votes:
            if vote.question_id not in user_votes:
                user_votes[vote.question_id] = []
            user_votes[vote.question_id].append(vote.choice_id)
    
    context = {
        'category': category,
        'polls': polls,
        'user_votes': user_votes,
    }
    return render(request, 'polls/category.html', context)
    