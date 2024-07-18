from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

router = DefaultRouter()

router.register(
    r'user',
    views.UserViewSet,
    basename='user'
)


urlpatterns = [
    path('', include(router.urls)),
]
