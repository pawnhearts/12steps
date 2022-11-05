from django.contrib.auth.decorators import login_required
from django.urls import path
from guide import views

urlpatterns = [
    path('/steps/', login_required(views.StepListView.as_view()), name='step-list'),
    path('/steps/<int:pk>/', login_required(views.StepDetailView.as_view()), name='step-detail'),
]
