from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from guide import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='guide/index.html')),
    path('steps/', views.StepListView.as_view(), name='step-list'),
    path('steps/<int:pk>/', views.QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', login_required(views.AnswerCreateView.as_view()), name='answer-create'),
]
