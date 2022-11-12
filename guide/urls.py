from django.urls import path
from django.views.generic import TemplateView

from guide import views

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    path('steps/<str:program>/', views.StepListView.as_view(), name='step-list'),
    path('step/<int:pk>/', views.SectionListView.as_view(), name='section-list'),
    path('questions/<int:pk>/', views.QuestionListView.as_view(), name='question-list'),
    path('section/<int:pk>/', views.SectionDetailView.as_view(), name='section-detail'),
    path('question/<int:pk>/', views.AnswerCreateView.as_view(), name='answer-create'),
    path('answer/<int:pk>/', views.AnswerUpdateView.as_view(), name='answer-update'),
    path('answer/<int:pk>/delete/', views.AnswerDeleteView.as_view(), name='answer-delete'),
    path('question/<int:pk>/close/', views.AnswerCloseView.as_view(), name='answer-close'),
]
