from django.contrib import admin
from questions.models import Question, Option, Message

# Register your models here.

class OptionInline(admin.TabularInline):  
    model = Option  
    extra = 0

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display =  ['question_text']
    search_fields =  ['question_text']
    inlines = [OptionInline, MessageInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Message)