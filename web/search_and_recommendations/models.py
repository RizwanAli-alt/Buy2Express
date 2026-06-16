from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class SearchQuery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='search_queries')
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),       # ✅ user's search history
            models.Index(fields=['-timestamp']), # ✅ recent searches first
        ]

class Recommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recommendations')
    product = models.ForeignKey('product_management.Product', on_delete=models.CASCADE, related_name='recommended_products')
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),          # ✅ fetch recommendations for user
            models.Index(fields=['user', '-score']), # ✅ top recommendations first
        ]