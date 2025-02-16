from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Question
from .forms import QuestionForm

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'questions/question_detail.html', {'question': question})

@login_required
def question_new(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'questions/question_edit.html', {'form': form})

@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'questions/question_edit.html', {'form': form})

@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect('question_list')