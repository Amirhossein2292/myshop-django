from django.urls import path
from .views import OrderListAPIView, OrderDetailAPIView, download_pdf_view

app_name = "orders"

urlpatterns = [
    path("", OrderListAPIView.as_view(), name="order_list"),
    path("<str:order_id>/", OrderDetailAPIView.as_view(), name="order_detail"),
    path(
        "order/download_pdf/<str:order_id>/",
        download_pdf_view,
        name="order_download_pdf",
    ),
]
