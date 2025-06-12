import random
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from questions.models import Question
from quizzleef.serializers import QuestionSerializer


def home(request):
    return render(request, 'home.html')

@api_view(['GET'])
def get_question_by_id(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)

    serializer = QuestionSerializer(question)
    return Response(serializer.data)

@api_view(['GET'])
def get_random_question_by_category(request, category_id):
    questions = Question.objects.filter(category=category_id)
    if not questions:
        return Response({'error': 'Question not found for this category'}, status=404)
    question = random.choice(questions)
    serializer = QuestionSerializer(question)
    return Response(serializer.data)
