from rest_framework import viewsets

from .models import Discipline, Event, Offer
from .serializers import DisciplineSerializer, EventSerializer, OfferSerializer


class DisciplineViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_versions = ["v1"]
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_versions = ["v1"]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_versions = ["v1"]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
