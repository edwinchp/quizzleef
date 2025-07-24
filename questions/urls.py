from django.urls import path
from quizzleef import views
from .views import QuestionListView, QuestionViewForm


urlpatterns = [
    path('', QuestionListView.as_view(), name='list_questions'),
    path('agregar/', QuestionViewForm.as_view(), name='agregar'),
    path('api/question/<int:pk>', views.get_question_by_id, name='get_question_by_id'),
    path('api/random-question/', views.get_random_question,
         name='get_random_question'),  # Example: /api/random-question/?category=ISTQB&difficulty=easy
]