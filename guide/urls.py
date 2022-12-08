from django.urls import path, re_path

from guide import views

urlpatterns = [
    path('steps/<str:program>/', views.StepListView.as_view(), name='step-list'),
    # path('questions/<int:pk>/', views.SectionListView.as_view(), name='section-list'),
    path('steps/questions/<int:pk>/', views.QuestionListView.as_view(), name='question-list'),
    path('steps/section/<int:pk>/', views.SectionDetailView.as_view(), name='section-detail'),
    path('steps/question/<int:pk>/', views.AnswerCreateView.as_view(), name='answer-create'),
    path('steps/answer/<int:pk>/', views.AnswerUpdateView.as_view(), name='answer-update'),
    path('answer/<int:pk>/delete/', views.AnswerDeleteView.as_view(), name='answer-delete'),
    path('question/<int:pk>/close/', views.AnswerCloseView.as_view(), name='question-close'),
    re_path(r'^vote/(?P<pk>\d+)/(?P<vote>up|down)/$', views.AnswerVoteView.as_view(), name='answer-vote'),
]
