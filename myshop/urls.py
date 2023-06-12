from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("products.urls")),
    path("api/", include("app_users.urls")),
    path(
        "api/orders/", include("orders.urls")
    ),  # Add this line to include orders app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
