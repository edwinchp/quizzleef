from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from questions.models import Question, Option, Message, Category, CodeSnippet

# Register your models here.


class OptionInline(admin.TabularInline):  
    model = Option  
    extra = 1
    classes = ('collapse',)

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    classes = ('collapse',)



class CodeSnippetInline(admin.StackedInline):
    model = CodeSnippet
    extra = 0
    max_num = 1
    classes = ('collapse',)


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ['title', 'question_text', 'ready']
    list_filter = ['category']
    search_fields = ['title', 'question_text']
    inlines = [OptionInline, MessageInline, CodeSnippetInline]
    change_form_template = 'admin/change_form_with_clone.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:question_id>/clone/',
                self.admin_site.admin_view(self.clone_question),
                name='clone-question',
            ),
        ]
        return custom_urls + urls
    
    def clone_question(self, request, question_id):
        try:
            original = Question.objects.get(id=question_id)
            original.id = None  # This will create a new record
            original.save()
            
            # Clone related options
            for option in Option.objects.filter(question_id=question_id):
                option.id = None
                option.question = original
                option.save()
                
            # Clone related messages
            for message in Message.objects.filter(question_id=question_id):
                message.id = None
                message.question = original
                message.save()
            
            messages.success(request, 'Question cloned successfully!')
            return HttpResponseRedirect(
                reverse('admin:questions_question_change', args=[original.id])
            )
        except Question.DoesNotExist:
            messages.error(request, 'Original question not found')
            return HttpResponseRedirect(reverse('admin:questions_question_changelist'))

class CategoryAdmin(admin.ModelAdmin):
    model = Category

admin.site.register(Question, QuestionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CodeSnippet)

# Global admin branding
admin.site.site_header = "Quizzleef Administration"
admin.site.site_title = "Quizzleef Admin"
admin.site.index_title = "Manage Questions and Content"
