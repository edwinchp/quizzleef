from django.views import generic

from questions.models import Question
from .forms import QuestionForm


class QuestionViewForm(generic.FormView):
    form_class = QuestionForm
    template_name = "questions/add_question.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class QuestionListView(generic.ListView):
    model = Question
    template_name = "questions/list_questions.html"
    context_object_name = "questions"
    paginate_by = 10
