from rest_framework import serializers
from .models import Order, OrderItem
from django.utils import formats


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    subtotal = serializers.SerializerMethodField()

    def get_subtotal(self, obj):
        return self.format_currency(obj.subtotal())

    def format_currency(self, amount):
        return f"{formats.number_format(amount, decimal_pos=2, force_grouping=True)} "

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return self.format_currency(obj.total)

    def format_currency(self, amount):
        return f"{formats.number_format(amount, decimal_pos=2, force_grouping=True)} "

    class Meta:
        model = Order
        fields = [
            "order_id",
            "user",
            "created_at",
            "billing_address_line_1",
            "note",
            "city",
            "postal_code",
            "status",
            "is_paid",
            "telephone_number",
            "order_items",
            "total",
        ]
