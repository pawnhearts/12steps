from django.contrib.flatpages.models import FlatPage
from rest_framework import serializers

from guide.models import Sect, Question, Feeling


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


class FeelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeling
        fields = '__all__'
        read_only_fields = ('user',)
