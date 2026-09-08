from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample, inline_serializer
from django.core.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json

from quizzleef.serializers import QuestionSerializer, QuestionCreateSerializer
from .services import (
    get_question_by_id_service,
    get_random_questions_service,
    VALID_DIFFICULTIES,
    create_question_service,
)
from questions.models import Question


@extend_schema(
    description="Retrieve a single question by its primary key.",
    responses={
        200: OpenApiResponse(QuestionSerializer, description="The requested question"),
        404: OpenApiResponse(description="Question not found"),
    },
)
@api_view(["GET"])
def get_question_by_id(request, pk):
    try:
        question = get_question_by_id_service(pk)
    except Question.DoesNotExist:
        return Response({"error": "Question not found"}, status=404)

    serializer = QuestionSerializer(question)
    return Response(serializer.data)


@extend_schema(
    description="Retrieve a random question from a given category and difficulty.",
    parameters=[
        OpenApiParameter(name="category", type=str, location=OpenApiParameter.QUERY, description="Category name", required=True),
        OpenApiParameter(name="difficulty", type=str, location=OpenApiParameter.QUERY, description="Difficulty level", required=True, enum=VALID_DIFFICULTIES),
        OpenApiParameter(name="count", type=int, location=OpenApiParameter.QUERY, description="Number of questions to return", required=False),
    ],
    responses={
        200: OpenApiResponse(QuestionSerializer(many=True), description="A list of random questions"),
        400: OpenApiResponse(description="Missing or invalid parameters"),
        404: OpenApiResponse(description="Questions not found"),
        500: OpenApiResponse(description="Server error"),
    },
)
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


@extend_schema(
    description="Create a single question. Accepts JSON, multipart/form-data, or form data. An optional `metadata` nested object may be merged into the payload.",
    request={
        "application/json": QuestionCreateSerializer,
        "multipart/form-data": QuestionCreateSerializer,
        "application/x-www-form-urlencoded": QuestionCreateSerializer,
    },
    examples=[
        OpenApiExample(
            name="Create question",
            summary="Minimal question creation",
            value={
                "title": "testswagger",
                "question_text": "string",
                "short_explanation": "string",
                "photo": "string",
                "photo_caption": "string",
                "photo_spoiler": True,
                "difficulty": "easy",
                "hint": "string",
                "category_name": "test",
                "ready": False,
            },
            request_only=True,
        ),
    ],
    responses={
        201: OpenApiResponse(QuestionSerializer, description="Question created"),
        400: OpenApiResponse(description="Invalid metadata JSON or validation error"),
        500: OpenApiResponse(description="Server error"),
    },
)
@api_view(["POST"])
def create_question(request):

    data = request.data.copy()

    if "metadata" in data:
        raw = data.get("metadata")
        try:
            if isinstance(raw, dict):
                metadata = raw
            elif isinstance(raw, bytes):
                metadata = json.loads(raw.decode("utf-8"))
            elif isinstance(raw, str):
                metadata = json.loads(raw)
            else:
                raise ValueError("Unsupported metadata type: {}".format(type(raw)))
        except Exception as e:
            return Response({"error": f"Invalid metadata JSON: {str(e)}"}, status=400)
        # merge metadata into data (metadata fields override top-level ones)
        data.update(metadata)

    try:
        question = create_question_service(data)
    except ValidationError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    serializer = QuestionSerializer(question)
    return Response(serializer.data, status=201)


@extend_schema(
    description="Bulk-create questions. Accepts either a JSON list of question objects or an object with an `items` list. Returns per-item results with 201 on full success and 207 on partial success.",
    request=inline_serializer(
        name="BulkCreateRequest",
        fields={"items": serializers.ListField(child=serializers.DictField(), required=False)},
    ),
    responses={
        201: OpenApiResponse(description="All questions created"),
        207: OpenApiResponse(description="Partial success: some questions failed"),
        400: OpenApiResponse(description="Expected a list of question objects or an object with 'items' as a list"),
    },
)
@api_view(["POST"])
def create_questions_bulk(request):
    payload = request.data
    # Accept either a list of question dicts or an object with an 'items' list
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict) and isinstance(payload.get('items'), list):
        items = payload.get('items')
    else:
        return Response({
            'error': "Expected a list of question objects or an object with 'items' as a list"
        }, status=400)

    results = []
    success = 0
    errors = 0

    for idx, item in enumerate(items):
        data = dict(item or {})
        # Support per-item metadata merge similar to single create endpoint
        if 'metadata' in data:
            raw = data.get('metadata')
            try:
                if isinstance(raw, dict):
                    metadata = raw
                elif isinstance(raw, bytes):
                    metadata = json.loads(raw.decode('utf-8'))
                elif isinstance(raw, str):
                    metadata = json.loads(raw)
                else:
                    raise ValueError(f"Unsupported metadata type: {type(raw)}")
            except Exception as e:
                results.append({'index': idx, 'error': f'Invalid metadata JSON: {str(e)}'})
                errors += 1
                continue
            data.update(metadata)

        try:
            question = create_question_service(data)
            results.append({'index': idx, 'data': QuestionSerializer(question).data})
            success += 1
        except ValidationError as e:
            results.append({'index': idx, 'error': str(e)})
            errors += 1
        except Exception as e:
            results.append({'index': idx, 'error': str(e)})
            errors += 1

    status_code = 201 if errors == 0 else 207
    return Response({'success': success, 'errors': errors, 'results': results}, status=status_code)
