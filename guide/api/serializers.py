from django.contrib.flatpages.models import FlatPage
from rest_framework import serializers

from guide.models import Sect, Question


class SectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sect
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class FlatPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatPage
        fields = '__all__'
