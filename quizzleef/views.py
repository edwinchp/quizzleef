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
def get_random_question(request):
    # Get query parameters
    category_name = request.query_params.get('category')
    difficulty = request.query_params.get('difficulty')
    
    # Validate required fields
    if not all([category_name, difficulty]):
        return Response(
            {'error': 'Missing required parameters. Please provide both category and difficulty as query parameters.'},
            status=400
        )
    
    # Validate difficulty
    valid_difficulties = ['easy', 'medium', 'hard']
    if difficulty not in valid_difficulties:
        return Response(
            {'error': f'Invalid difficulty. Must be one of: {valid_difficulties}'},
            status=400
        )
    
    try:
        # Get questions filtered by category name and difficulty
        questions = Question.objects.filter(
            category__name__iexact=category_name,
            difficulty=difficulty
        )
        
        if not questions.exists():
            return Response(
                {'error': f'No questions found for category: {category_name} and difficulty: {difficulty}'},
                status=404
            )
            
        # Select a random question from the filtered queryset
        question = random.choice(questions)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=500
        )
