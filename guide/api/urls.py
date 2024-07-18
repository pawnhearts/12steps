from django.urls import path

from .views import SectListAPIView, QuestionListAPIView, FlatPageListAPIView

urlpatterns = [
    path('pages/', FlatPageListAPIView.as_view()),
    path('sects/', SectListAPIView.as_view()),
    path('questions/', QuestionListAPIView.as_view()),
]