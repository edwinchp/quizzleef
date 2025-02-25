from django.urls import path
from . import views
from .views import QuestionViewForm

urlpatterns = [
    path('agregar/', QuestionViewForm.as_view(), name='agregar'),
]