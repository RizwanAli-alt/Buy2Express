from django.db import models


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Card', 'Card'),
        ('COD', 'Cash on Delivery'),
        ('Wallet', 'Wallet'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    order = models.OneToOneField(
        'cart_and_orders.Order',
        on_delete=models.CASCADE,
        related_name='payment'
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.payment_status}"

    def is_successful(self):
        """Checks if the payment was successful."""
        return self.payment_status == 'Completed'
