from django.db import models

class Review(models.Model):
    product = models.ForeignKey('product_management.Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    review_images = models.ImageField(upload_to="reviews/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['product']),               # ✅ all reviews for a product
            models.Index(fields=['user']),                  # ✅ all reviews by a user
            models.Index(fields=['product', 'is_approved']),# ✅ approved reviews only
            models.Index(fields=['-created_at']),           # ✅ newest reviews first
        ]