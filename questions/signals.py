from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
from .models import Question

@receiver(pre_delete, sender=Question)
def delete_question_file(sender, instance, **kwargs):
    """
    Deletes the associated image file when a Question is deleted.
    """
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)
