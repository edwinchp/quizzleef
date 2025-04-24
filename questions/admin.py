from django.contrib import admin
from questions.models import Question, Option

# Register your models here.

class OptionInline(admin.TabularInline):  
    model = Option  
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display =  ['question_text', 'answer']
    search_fields =  ['question_text']
    inlines = [OptionInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)