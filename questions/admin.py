from django.contrib import admin
from questions.models import Question

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display =  ['question_text', 'answer']
    search_fields =  ['question_text']

admin.site.register(Question, QuestionAdmin)