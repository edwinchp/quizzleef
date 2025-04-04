from django.db import models

class Question(models.Model):
    question_text = models.TextField(help_text="Enter question text.")
    answer = models.CharField(max_length=1, help_text="Correct option (e.g., 'a', 'b', 'c', 'd')")
    explanation = models.TextField(blank=True, null=True, help_text="Explanation for the correct answer")
    photo = models.FileField(null=True, upload_to='questions/pictures', blank=True)

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    option_text = models.TextField(help_text="Enter option text")
    option_letter = models.CharField(max_length=1, help_text="Option identifier (e.g., 'a', 'b', 'c', 'd')")

    def __str__(self):
        return f"{self.option_letter}: {self.option_text}"