from django.db import models
from django.contrib.auth import get_user_model


CustomUser = get_user_model()

class SearchQuery(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='search_queries'
    )
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search by {self.user.username}: {self.query}"

class Recommendation(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    product = models.ForeignKey(
        'product_management.Product',
        on_delete=models.CASCADE,
        related_name='recommended_products'
    )
    score = models.FloatField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.user.username} - {self.product.name} (Score: {self.score})"
