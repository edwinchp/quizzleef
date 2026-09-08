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


class QuestionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(help_text="Question title (required)")
    question_text = serializers.CharField(help_text="Question text (required)")
    short_explanation = serializers.CharField(required=False, allow_blank=True)
    photo = serializers.CharField(required=False, allow_blank=True, help_text="Photo file name or URL")
    photo_caption = serializers.CharField(required=False, allow_blank=True)
    photo_spoiler = serializers.BooleanField(required=False)
    difficulty = serializers.ChoiceField(choices=["easy", "medium", "hard"], required=False)
    hint = serializers.CharField(required=False, allow_blank=True)
    category_name = serializers.CharField(required=False, help_text="Category name (case-insensitive)")
    category_id = serializers.IntegerField(required=False, help_text="Alternative to category_name")
    ready = serializers.BooleanField(required=False)
    options = OptionSerializer(many=True, required=False)
    messages = MessageSerializer(many=True, required=False)
    code_snippet = CodeSnippetSerializer(required=False)