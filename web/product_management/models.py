from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)  # unique=True auto-indexes
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="subcategories")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    def __str__(self):
        return self.name

class Seller(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # unique=True auto-indexes
    profile_image = models.ImageField(upload_to="sellers/", blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['is_verified']),  # ✅ filter verified sellers
            models.Index(fields=['-rating']),       # ✅ top-rated sellers
        ]

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)  # unique=True auto-indexes
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['category']),              # ✅ browse by category
            models.Index(fields=['seller']),                # ✅ seller's product listings
            models.Index(fields=['is_active']),             # ✅ show only active products
            models.Index(fields=['is_featured']),           # ✅ homepage featured section
            models.Index(fields=['category', 'is_active']), # ✅ composite: active products in category
            models.Index(fields=['price']),                 # ✅ price sorting/filtering
            models.Index(fields=['-created_at']),           # ✅ newest first
        ]

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")

    class Meta:
        indexes = [
            models.Index(fields=['product']),  # ✅ fetch all images for a product
        ]

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    key = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['product']),  # ✅ fetch all specs for a product
        ]

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=255)
    options = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['product']),  # ✅ fetch all variants for a product
        ]