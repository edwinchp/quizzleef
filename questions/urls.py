from django.urls import path
from . import views
from .views import QuestionListView, QuestionViewForm

urlpatterns = [
    path('', QuestionListView.as_view(), name='list_questions'),
    path('agregar/', QuestionViewForm.as_view(), name='agregar'),
]