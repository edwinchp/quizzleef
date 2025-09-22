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

    validate_difficulty(difficulty)

    filters = {"category__name__iexact": category_name}
    if difficulty != "any":
        filters["difficulty"] = difficulty

    return Question.objects.filter(**filters)


def get_question_by_id_service(pk: int) -> Question:
    return Question.objects.get(pk=pk)


def get_random_questions_service(category_name: str, difficulty: str, count: int = 1) -> list[Question]:
    if not category_name:
        raise ValidationError("Missing required parameter: category")
    if not difficulty:
        raise ValidationError("Missing required parameter: difficulty")
    if count is None or int(count) < 1:
        raise ValidationError("'count' must be a positive integer")

    qs = get_questions_queryset(category_name, difficulty)
    total = qs.count()

    if total == 0:
        raise Question.DoesNotExist(
            f"No questions found for category: {category_name} and difficulty: {difficulty}"
        )

    # Ensure we don't request more than available; sample without replacement
    k = min(int(count), total)
    # Convert to list once to avoid multiple DB hits and to use random.sample
    questions_list = list(qs)
    return random.sample(questions_list, k)