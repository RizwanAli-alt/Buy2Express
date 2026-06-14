from django.db import models
from django.utils import timezone

class Deal(models.Model):
    product = models.ForeignKey('product_management.Product', on_delete=models.CASCADE, related_name='deals')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Deal: {self.title}"

    def is_expired(self):
        return self.end_date < timezone.now()

    def is_valid(self):
        return self.is_active and self.start_date <= timezone.now() <= self.end_date


class Discount(models.Model):
    product = models.ForeignKey('product_management.Product', on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_percentage}% Discount on {self.product.name}"

    def is_expired(self):
        return self.end_date < timezone.now()

    def is_valid(self):
        return self.is_active and self.start_date <= timezone.now() <= self.end_date


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_expired(self):
        return self.valid_until < timezone.now()
    
    def is_valid(self):
        return self.active and self.valid_from <= timezone.now() <= self.valid_until