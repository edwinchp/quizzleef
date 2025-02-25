from django.views import generic
from .forms import QuestionForm

class QuestionViewForm(generic.FormView):
    form_class = QuestionForm
    template_name = 'questions/add_question.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

