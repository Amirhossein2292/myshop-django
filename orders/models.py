from django.db import models
from app_users.models import AppUser
from products.models import Product
import uuid
from django.utils import formats


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("checked", "Checked"),
        ("delivered", "Delivered"),
        ("received", "Received"),
    ]

    order_id = models.CharField(max_length=20, primary_key=True, editable=False)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    billing_address_line_1 = models.CharField(max_length=100, null=True)
    note = models.TextField(blank=True, null=True)
    city_choices = [
        ("Tehran", "Tehran"),
        ("Karaj", "Karaj"),
        ("Fardis", "Fardis"),
    ]
    city = models.CharField(max_length=50, choices=city_choices, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    is_paid = models.BooleanField(default=False, null=True)
    telephone_number = models.CharField(max_length=20, null=True)
    total = models.CharField(max_length=20, default="0")

    def calculate_total(self):
        order_items = self.order_items.all()
        total = sum(item.subtotal_decimal() for item in order_items)
        return total

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = str(uuid.uuid4()).split("-")[0]
        self.total = self.format_total(self.calculate_total())
        super().save(*args, **kwargs)

    def format_total(self, total):
        return formats.number_format(total, decimal_pos=3, force_grouping=True)

    def __str__(self):
        return f"Order {self.order_id} - User: {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def subtotal_decimal(self):
        subtotal = self.quantity * self.product.price
        return subtotal

    def subtotal(self):
        subtotal = self.subtotal_decimal()
        return self.format_subtotal(subtotal)

    def format_subtotal(self, subtotal):
        return formats.number_format(subtotal, decimal_pos=2, force_grouping=True)

    def __str__(self):
        return f"Order ID: {self.order.order_id}, Product: {self.product.name}, Quantity: {self.quantity}, User: {self.order.user.username}"
