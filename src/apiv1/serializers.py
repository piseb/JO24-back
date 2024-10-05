from rest_framework import serializers

from .models import Discipline, Event


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "discipline", "title", "begin_at", "end_at", "description"]
