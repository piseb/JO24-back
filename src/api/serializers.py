from rest_framework import serializers

from .models import Discipline, Event, Offer


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ["uuid", "name"]


class EventSerializer(serializers.ModelSerializer):
    # insert directly the serialized discipline values (nested serialized)
    discipline = DisciplineSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ["uuid", "discipline", "title", "begin_at", "end_at", "description"]


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ["uuid", "title", "description", "price", "ntickets", "disable"]
