from rest_framework import viewsets

from .models import Discipline, Event
from .serializers import DisciplineSerializer, EventSerializer


class DisciplineViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_versions = ["v1"]
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_versions = ["v1"]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
