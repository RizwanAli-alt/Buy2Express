from django.db import models

class Wishlist(models.Model):
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('product_management.Product', on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),            # ✅ user's wishlist
            models.Index(fields=['user', 'product']), # ✅ check if product is wishlisted
        ]
        unique_together = ['user', 'product']         # ✅ prevent duplicate wishlist entries

class FavoriteStore(models.Model):
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, related_name='favorite_stores')
    seller = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),  # ✅ user's favorite stores
        ]
        unique_together = ['user', 'seller']  # ✅ prevent duplicates