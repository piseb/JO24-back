from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Discipline, Event, Offer
from .serializers import DisciplineSerializer, EventSerializer, OfferSerializer


class DisciplineViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    allowed_versions = ["v1"]
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    allowed_versions = ["v1"]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    allowed_versions = ["v1"]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OfferEnableViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    allowed_versions = ["v1"]
    queryset = Offer.objects.filter(disable=False)
    serializer_class = OfferSerializer  # no need another serializer


class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    allowed_versions = ["v1"]

    def create(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            return Response(status="401")
        try:
            # user profile must exist for api user
            user.user_profile
        except ObjectDoesNotExist:
            return Response(status="401")

        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={"token": token.key})


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            token = Token.objects.get(user=request.user)
            if token:
                token.delete()
            return Response(status="200")
        except Token.DoesNotExist:
            pass
        return Response(status="401")
