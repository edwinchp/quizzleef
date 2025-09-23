from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from quizzleef.serializers import QuestionSerializer
from .services import (
    get_question_by_id_service,
    get_random_questions_service,
    VALID_DIFFICULTIES,
    create_question_service,
)
from questions.models import Question


@api_view(["GET"])
def get_question_by_id(request, pk):
    try:
        question = get_question_by_id_service(pk)
    except Question.DoesNotExist:
        return Response({"error": "Question not found"}, status=404)

    serializer = QuestionSerializer(question)
    return Response(serializer.data)


@api_view(["GET"])
def get_random_question(request):
    category_name = request.query_params.get("category")
    difficulty = request.query_params.get("difficulty")
    count = request.query_params.get("count") or 1

    if not all([category_name, difficulty]):
        return Response(
            {
                "error": "Missing required parameters. Please provide both category and difficulty as query parameters.",
            },
            status=400,
        )

    try:
        questions = get_random_questions_service(category_name, difficulty, count=count)
    except ValidationError as e:
        return Response({"error": str(e)}, status=400)
    except Question.DoesNotExist as e:
        return Response({"error": str(e)}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_question(request):

    data = request.data.copy()

    if hasattr(request, "FILES") and request.FILES.get("photo"):
        data["photo"] = request.FILES.get("photo")

    try:
        question = create_question_service(data)
    except ValidationError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    serializer = QuestionSerializer(question)
    return Response(serializer.data, status=201)