from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # API documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # API routes
    path("api/auth/", include("apps.accounts.urls")),
    path("api/books/", include("apps.books.urls")),
    path("api/circulations/", include("apps.circulations.urls")),
    path("api/fines/", include("apps.fines.urls")),
]
