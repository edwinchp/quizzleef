# Generated by Django 5.1.6 on 2025-03-08 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_alter_question_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='photo',
            field=models.FileField(null=True, upload_to='media/questions'),
        ),
    ]
