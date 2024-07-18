from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from users.api.serializers import UserSerializer



class UserViewSet(viewsets.ViewSet):

    queryset = Note.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        validated_data = request.data

        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()

        user_serializered = UserSerializer(user)

        return Response(user_serializered.data)
