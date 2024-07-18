from django.contrib.flatpages.models import FlatPage
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView
from .serializers import SectSerializer, QuestionSerializer, FlatPageSerializer
from ..models import Sect


class SectListAPIView(ListAPIView):
    queryset = Sect.objects.filter(is_active=True)
    serializer_class = SectSerializer

class QuestionListAPIView(ListAPIView):
    def get_queryset(self):
        # qs = super().get_queryset().select_related('section').filter(section__step_id=self.kwargs.get('pk'))
        qs = super().get_queryset().select_related('section').filter(
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