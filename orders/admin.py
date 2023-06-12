from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "status", "download_pdf_link")

    def download_pdf_link(self, obj):
        pdf_url = reverse("orders:order_download_pdf", args=[obj.order_id])
        return format_html('<a href="{}">Download PDF</a>', pdf_url)

    download_pdf_link.short_description = "Download PDF"


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
