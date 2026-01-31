from django.db import models
from django.contrib.auth.models import User

# Question class
class Question(models.Model):
    question_text = models.CharField(max_length = 300)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    """Track which user voted for which choice"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')  # One vote per user per question
        ordering = ['-voted_at']
    
    def __str__(self):
        return f"{self.user.username} voted for {self.choice.choice_text}"