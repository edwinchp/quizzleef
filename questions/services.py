from typing import Optional
import random

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from questions.models import Question


VALID_DIFFICULTIES = ["easy", "medium", "hard", "any"]


def validate_difficulty(difficulty: str) -> None:
    if difficulty not in VALID_DIFFICULTIES:
        raise ValidationError(
            f"Invalid difficulty. Must be one of: {VALID_DIFFICULTIES}"
        )


def get_questions_queryset(category_name: str, difficulty: str) -> QuerySet[Question]:
    """
    Build the queryset for questions based on category and difficulty.
    """
    validate_difficulty(difficulty)

    filters = {"category__name__iexact": category_name}
    if difficulty != "any":
        filters["difficulty"] = difficulty

    return Question.objects.filter(**filters)


def get_question_by_id_service(pk: int) -> Question:
    return Question.objects.get(pk=pk)


def get_random_question_service(category_name: str, difficulty: str) -> Question:
    if not category_name:
        raise ValidationError("Missing required parameter: category")
    if not difficulty:
        raise ValidationError("Missing required parameter: difficulty")

    qs = get_questions_queryset(category_name, difficulty)
    if not qs.exists():
        # Raise DoesNotExist to keep familiar semantics for callers
        raise Question.DoesNotExist(
            f"No questions found for category: {category_name} and difficulty: {difficulty}"
        )

    return random.choice(list(qs))
