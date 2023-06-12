from django.db import models
from django.utils import formats


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="product_images/", null=True)  # Add this line
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    def format_price(self):
        return formats.number_format(
            float(self.price), decimal_pos=2, force_grouping=True
        )

    def __str__(self):
        return self.name
