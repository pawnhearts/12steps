from django.contrib.flatpages.models import FlatPage
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView, ListCreateAPIView
from .serializers import SectSerializer, QuestionSerializer, FlatPageSerializer, FeelingSerializer
from ..models import Sect, Question


class SectListAPIView(ListAPIView):
    queryset = Sect.objects.filter(is_visible=True)
    serializer_class = SectSerializer


class QuestionListAPIView(ListAPIView):
    def get_queryset(self):
        # qs = super().get_queryset().select_related('section').filter(section__step_id=self.kwargs.get('pk'))
        qs = Question.objects.select_related('section').filter(
            section__step__sect_id=self.kwargs.get('sect'),
            section__step__number=self.kwargs.get('step')
        )
        if self.request.user.is_authenticated:
            qs = qs.with_answer_count(self.request.user)
        qs = qs.order_by('section__step__number', 'section__number', 'number')
        return qs

    serializer_class = QuestionSerializer


class FlatPageListAPIView(ListAPIView):
    queryset = FlatPage.objects.all()
    serializer_class = FlatPageSerializer


class FeelingListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeelingSerializer

    def get_queryset(self):
        return self.queryset.filter(Q(user=None) | Q(user=self.request.user))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
