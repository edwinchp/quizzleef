from django.contrib import admin
from questions.models import Question, Option, Message, Category

# Register your models here.

class OptionInline(admin.TabularInline):  
    model = Option  
    extra = 0

class MessageInline(admin.TabularInline):
    model = Message
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display =  ['question_text']
    search_fields =  ['question_text']
    inlines = [OptionInline, MessageInline]

class CategoryAdmin(admin.ModelAdmin):
    model = Category

admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Message)
admin.site.register(Category, CategoryAdmin)