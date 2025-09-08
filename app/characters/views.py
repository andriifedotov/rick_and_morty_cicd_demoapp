import time
from typing import Dict
from django.core.cache import cache
from django.db import connection
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import Throttled, ValidationError
from rest_framework.settings import api_settings
from rest_framework.filters import OrderingFilter
from .models import Character
from .serializers import CharacterSerializer
from rest_framework.views import exception_handler


# ---- API Views ----

class CharacterListView(generics.ListAPIView):
    """Return characters already filtered to Human + Alive + Earth-origin.
    Supports ordering by ?ordering=name or ?ordering=id (prefix with - for desc).
    Data comes from DB (populated by sync command).
    """
    serializer_class = CharacterSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["name", "id"]

    def get_queryset(self):
        qs = Character.objects.filter(
            species__iexact="Human",
            status__iexact="Alive",
            origin_name__istartswith="Earth (",
        )
        # Enforce explicit ordering if provided; else model default
        ordering = self.request.query_params.get("ordering")
        if ordering and ordering.lstrip("-") not in self.ordering_fields:
            raise ValidationError({
                "ordering": f"Invalid field. Allowed: {', '.join(self.ordering_fields)}"
            })
        return qs

class HealthCheckView(APIView):
    """Deep health check: DB + cache roundtrip and optional timing."""

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        report: Dict[str, Dict] = {"status": "ok", "checks": {}}

        # DB connectivity
        try:
            with connection.cursor() as cur:
                cur.execute("SELECT 1;")
                row = cur.fetchone()
            report["checks"]["database"] = {"ok": row == (1,), "detail": str(row)}

        except Exception as e:
            report["status"] = "degraded"
            report["checks"]["database"] = {"ok": False, "error": str(e)}

        # Cache roundtrip

        try:
            key = "healthcheck:ping"
            cache.set(key, "pong", timeout=10)
            val = cache.get(key)
            report["checks"]["cache"] = {"ok": val == "pong"}
            if val != "pong":
                report["status"] = "degraded"

        except Exception as e:
            report["status"] = "degraded"
            report["checks"]["cache"] = {"ok": False, "error": str(e)}

        http_status = status.HTTP_200_OK if report["status"] == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(report, status=http_status)

# ---- Exception handler to surface nice 400/429/503 ----

def custom_exception_handler(exc, context):
    # First, call DRF's default exception handler
    response = exception_handler(exc, context)

    # Handle throttling errors with a custom response
    if isinstance(exc, Throttled):
        detail = {
            "detail": "Request was throttled. Reduce request rate.",
            "available_in": exc.wait,
        }
        return Response(detail, status=status.HTTP_429_TOO_MANY_REQUESTS)

    # If DRF produced a response, return it
    if response is not None:
        return response

    # Fallback for unexpected errors
    return Response(
        {"detail": "Service temporarily unavailable."},
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )