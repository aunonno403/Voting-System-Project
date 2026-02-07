from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Poll categories/tags for organization"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Question(models.Model):
    """Enhanced Question/Poll model with multiple features"""
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('password', 'Password Protected'),
    ]
    
    # Basic fields
    question_text = models.CharField(max_length=300)
    description = models.TextField(blank=True, help_text="Optional detailed description")
    pub_date = models.DateTimeField('date published')
    
    # Enhanced fields
    start_date = models.DateTimeField(null=True, blank=True, help_text="When poll becomes active")
    end_date = models.DateTimeField(null=True, blank=True, help_text="When poll closes")
    
    # Features
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    image = models.ImageField(upload_to='poll_images/', null=True, blank=True)
    
    # Settings
    is_draft = models.BooleanField(default=False, help_text="Draft polls are not visible to users")
    allow_multiple_choices = models.BooleanField(default=False, help_text="Allow users to select multiple options")
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    password = models.CharField(max_length=100, blank=True, help_text="Required if visibility is password protected")
    invited_users = models.ManyToManyField(User, blank=True, related_name='invited_polls', help_text="Users who can access this private poll")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_polls')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.question_text
    
    def is_active(self):
        """Check if poll is currently active"""
        now = timezone.now()
        if self.is_draft:
            return False
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True
    
    def is_upcoming(self):
        """Check if poll hasn't started yet"""
        if self.start_date and timezone.now() < self.start_date:
            return True
        return False
    
    def is_expired(self):
        """Check if poll has ended"""
        if self.end_date and timezone.now() > self.end_date:
            return True
        return False
    
    def total_votes(self):
        """Get total votes for this poll"""
        return self.vote_set.count()
    
    def can_user_access(self, user):
        """Check if a user can access this poll based on visibility settings"""
        if not user.is_authenticated:
            return self.visibility == 'public'
        
        # Draft polls only visible to creator
        if self.is_draft and self.created_by != user:
            return False
        
        # Public and password-protected polls are visible to all authenticated users
        if self.visibility in ['public', 'password']:
            return True
        
        # Private polls only visible to creator and invited users
        if self.visibility == 'private':
            return user == self.created_by or self.invited_users.filter(id=user.id).exists()
        
        return False
    
    def clean(self):
        """Validate model data"""
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        if self.visibility == 'password' and not self.password:
            raise ValidationError("Password is required for password-protected polls")


class Choice(models.Model):
    """Poll choice/option"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    description = models.TextField(blank=True, help_text="Optional description for this choice")
    image = models.ImageField(upload_to='choice_images/', null=True, blank=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.choice_text
    
    def vote_percentage(self):
        """Calculate percentage of votes"""
        total = self.question.choice_set.aggregate(models.Sum('votes'))['votes__sum'] or 0
        if total == 0:
            return 0
        return round((self.votes / total) * 100, 1)


class Vote(models.Model):
    """Track which user voted for which choice(s)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        # For single-choice polls, one vote per user per question
        # For multiple-choice, one vote per user per choice
        unique_together = ('user', 'choice')
        ordering = ['-voted_at']
    
    def __str__(self):
        return f"{self.user.username} voted for {self.choice.choice_text}"


class Comment(models.Model):
    """User comments on polls"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} on {self.question.question_text[:50]}"