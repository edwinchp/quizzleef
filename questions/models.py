from django.db import models

class Question(models.Model):
    messages = models.TextField(help_text="Enter message.")
    photo = models.FileField(null=True, upload_to='questions/pictures')
    question_text = models.TextField(help_text="Enter question text.")
    options = models.TextField(help_text="Enter options separated by newlines.")
    answer = models.CharField(max_length=1)
    explanation = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.question_text