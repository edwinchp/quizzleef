from django import forms
from .models import Question

class QuestionForm(forms.Form):
    messages = forms.CharField(widget=forms.TextInput(), required=False)
    photos = forms.CharField(widget=forms.TextInput(), required=False)
    question_text = forms.CharField(widget=forms.TextInput())
    options = forms.CharField(widget=forms.TextInput())
    answer = forms.CharField(max_length=1)
    explanation = forms.CharField(widget=forms.TextInput())

    def save(self):
        question = Question(
            messages=self.cleaned_data['messages'],
            photos=self.cleaned_data['photos'],
            question_text=self.cleaned_data['question_text'],
            options=self.cleaned_data['options'],
            answer=self.cleaned_data['answer'],
            explanation=self.cleaned_data['explanation']
        )
        question.save()
        return question