from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("disciplines", views.DisciplineViewSet)
router.register("events", views.EventViewSet)
# order line is important
router.register("offers/enable", views.OfferEnableViewSet, basename="offer-enable")
router.register("offers", views.OfferViewSet, basename="offer")

urlpatterns = [
    path("", include(router.urls)),
]

# if in DEBUG mode: add auto documentation from drf_spectacular
if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]
