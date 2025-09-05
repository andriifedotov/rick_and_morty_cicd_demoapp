from django.contrib import admin
from django.urls import path, include
from characters.views import HealthCheckView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("characters.urls")),
    path("healthcheck", HealthCheckView.as_view(), name="healthcheck"),
]