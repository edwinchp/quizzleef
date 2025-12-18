from rest_framework import serializers
from questions.models import Question, Option, CodeSnippet, Message

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']
        read_only_fields = ['id', 'option_text', 'is_correct']


class CodeSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet
        fields = ['title', 'content', 'language']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_text']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    code_snippet = CodeSnippetSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'question_text', 'short_explanation', 'photo', 'photo_caption', 
                 'photo_spoiler', 'difficulty', 'hint', 'category', 'ready', 'options', 'code_snippet', 'messages']