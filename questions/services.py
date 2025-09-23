from typing import Optional
import random

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.db import transaction

from questions.models import Question
from questions.models import Category, Option, Message


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


@transaction.atomic
def create_question_service(data: dict) -> Question:

    # Mandatory fields
    question_text = (data.get("question_text") or "").strip()
    if not question_text:
        raise ValidationError("'question_text' is required")

    category_id = data.get("category_id")
    category_name = data.get("category_name")
    category: Optional[Category] = None
    if category_id is not None:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError(f"Category with id={category_id} does not exist")
    elif category_name:
        try:
            category = Category.objects.get(name__iexact=category_name)
        except Category.DoesNotExist:
            raise ValidationError(f"Category with name='{category_name}' does not exist")
    else:
        raise ValidationError("Either 'category_id' or 'category_name' is required")

    # Optional fields
    difficulty = data.get("difficulty")
    if difficulty:
        validate_difficulty(difficulty)

    short_explanation = data.get("short_explanation")
    photo = data.get("photo")
    photo_caption = data.get("photo_caption")
    photo_spoiler = data.get("photo_spoiler")
    hint = data.get("hint")

    # Create the question
    question = Question.objects.create(
        question_text=question_text,
        category=category,
        difficulty=difficulty or Question._meta.get_field("difficulty").get_default(),
        short_explanation=short_explanation,
        photo=photo,
        photo_caption=photo_caption,
        photo_spoiler=photo_spoiler if photo_spoiler is not None else False,
        hint=hint,
    )

    # Create related options
    options = data.get("options") or []
    option_objs = []
    for opt in options:
        text = (opt.get("option_text") or "").strip()
        if not text:
            raise ValidationError("Each option must include non-empty 'option_text'")
        is_correct = bool(opt.get("is_correct", False))
        option_objs.append(Option(question=question, option_text=text, is_correct=is_correct))
    if option_objs:
        Option.objects.bulk_create(option_objs)

    # Create related messages
    messages = data.get("messages") or []
    msg_objs = []
    for msg in messages:
        text = (msg.get("message_text") or "").strip()
        if not text:
            raise ValidationError("Each message must include non-empty 'message_text'")
        msg_objs.append(Message(question=question, message_text=text))
    if msg_objs:
        Message.objects.bulk_create(msg_objs)

    return question