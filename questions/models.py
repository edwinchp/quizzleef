from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30, help_text="Max characters: 30")

    def __str__(self):
        return self.name


class Question(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Knowledge'),
        ('science', 'Science'),
        ('history', 'History'),
        ('geography', 'Geography'),
        ('entertainment', 'Entertainment'),
        ('sports', 'Sports'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]
    
    question_text = models.TextField(max_length=300, help_text="Max characters: 300")
    short_explanation = models.TextField(max_length=200, blank=True, null=True, help_text="Max characters: 200")
    photo = models.FileField(null=True, upload_to='questions/pictures', blank=True)
    photo_caption = models.TextField(max_length=300, blank=True, null=True, help_text="Max characters: 300")
    photo_spoiler = models.BooleanField(blank=True, default=False, choices=[(True, 'Yes'), (False, 'No')], help_text="Spoiler text for the photo")
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='easy', help_text="Select difficulty level")
    hint = models.TextField(blank=True, null=True, help_text="Hint for the question")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, related_name="options")
    option_text = models.TextField(max_length=100, help_text="Max characters: 100")
    is_correct = models.BooleanField(null=True, max_length=1, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Is this option correct?")

    def __str__(self):
        return f"{self.is_correct}: {self.option_text}"


class Message(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, related_name="messages")
    message_text = models.TextField(max_length=500, help_text="Max characters: 500")

    def __str__(self):
        return f"{self.message_text}"