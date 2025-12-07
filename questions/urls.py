from django.urls import path
from .views import QuestionListView, QuestionViewForm
from .api_views import get_question_by_id, get_random_question, create_question, create_questions_bulk


urlpatterns = [
    path('', QuestionListView.as_view(), name='list_questions'),
    path('agregar/', QuestionViewForm.as_view(), name='agregar'),
    path('api/question/<int:pk>', get_question_by_id, name='get_question_by_id'),
    path('api/random-question/', get_random_question,
         name='get_random_question'),
    path('api/questions/', create_question, name='create_question'),
    path('api/questions/bulk/', create_questions_bulk, name='create_questions_bulk'),

]
