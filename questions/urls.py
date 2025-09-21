from django.urls import path
from .views import QuestionListView, QuestionViewForm
from .api_views import get_question_by_id, get_random_question


urlpatterns = [
    path('', QuestionListView.as_view(), name='list_questions'),
    path('agregar/', QuestionViewForm.as_view(), name='agregar'),
    path('api/question/<int:pk>', get_question_by_id, name='get_question_by_id'),
    path('api/random-question/', get_random_question,
         name='get_random_question'),  # Example: /api/random-question/?category=ISTQB&difficulty=easy
]