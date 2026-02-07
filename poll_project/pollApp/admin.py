from django.contrib import admin
from .models import Question, Choice, Vote, Category, Comment

admin.site.site_header = "The Poll Mall"
admin.site.site_title = "Voting Admin Area"
admin.site.index_title = "Welcome to our Voting Admin Area"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3
    fields = ['choice_text', 'description', 'image', 'votes']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'category', 'is_draft', 'visibility', 'pub_date', 'is_active', 'total_votes']
    list_filter = ['is_draft', 'visibility', 'category', 'pub_date', 'created_at']
    search_fields = ['question_text', 'description']
    readonly_fields = ['created_at', 'updated_at', 'total_votes']
    filter_horizontal = ['invited_users']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['question_text', 'description', 'category', 'image']
        }),
        ('Date & Time', {
            'fields': ['pub_date', 'start_date', 'end_date'],
            'description': 'Control when poll is visible and active'
        }),
        ('Settings', {
            'fields': ['is_draft', 'visibility', 'password', 'allow_multiple_choices', 'invited_users'],
            'classes': ['collapse'],
            'description': 'For private polls, select users who should have access'
        }),
        ('Metadata', {
            'fields': ['created_by', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    inlines = [ChoiceInLine]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'votes', 'vote_percentage']
    list_filter = ['question']
    search_fields = ['choice_text', 'question__question_text']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'choice', 'voted_at']
    list_filter = ['voted_at', 'question']
    search_fields = ['user__username', 'question__question_text']
    readonly_fields = ['voted_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'text_preview', 'created_at', 'is_edited']
    list_filter = ['created_at', 'is_edited']
    search_fields = ['user__username', 'question__question_text', 'text']
    readonly_fields = ['created_at', 'updated_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'