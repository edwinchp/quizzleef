from rest_framework import serializers
from questions.models import Question, Option, CodeSnippet

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']
        read_only_fields = ['id', 'option_text', 'is_correct']


class CodeSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet
        fields = ['title', 'content', 'language']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    code_snippet = CodeSnippetSerializer(read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'short_explanation', 'photo', 'photo_caption', 
                 'photo_spoiler', 'difficulty', 'hint', 'category', 'options', 'code_snippet']