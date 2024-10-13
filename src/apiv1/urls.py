from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"disciplines", views.DisciplineViewSet)
router.register(r"events", views.EventViewSet)

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
