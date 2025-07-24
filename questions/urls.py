from django.urls import path
from quizzleef import views
from .views import QuestionListView, QuestionViewForm


urlpatterns = [
    path('', QuestionListView.as_view(), name='list_questions'),
    path('agregar/', QuestionViewForm.as_view(), name='agregar'),
    path('api/question/<int:pk>', views.get_question_by_id, name='get_question_by_id'),
    path('api/random-question/<int:category_id>', views.get_random_question_by_category,
         name='get_random_question_by_category'),
]