from django.contrib import admin
from .models import Question, Choice, Vote

admin.site.site_header = "The Poll Mall"
admin.site.site_title = "Voting Admin Area"
admin.site.index_title = "Welcome to our Voting Admin Area"

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['question_text']}), ('Date Information', {'fields': ['pub_date'], 'classes':['collapse']}),]
    inlines = [ChoiceInLine]

class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'choice', 'voted_at']
    list_filter = ['voted_at', 'question']
    search_fields = ['user__username', 'question__question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote, VoteAdmin)