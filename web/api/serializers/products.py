"""Product, Category, Brand serializers."""
from rest_framework import serializers
from product_management.models import Product, Category, Brand, ProductImage, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug', 'image']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Brand
        fields = ['id', 'name', 'logo']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductVariant
        fields = ['id', 'name', 'value', 'price_modifier', 'stock']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    category = serializers.StringRelatedField()
    brand    = serializers.StringRelatedField()

    class Meta:
        model  = Product
        fields = ['id', 'name', 'slug', 'price', 'category', 'brand', 'thumbnail', 'is_active']


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for product detail view."""
    category = CategorySerializer(read_only=True)
    brand    = BrandSerializer(read_only=True)
    images   = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    # Write-only FK fields for create/update
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source='brand', write_only=True, required=False
    )

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'stock',
            'category', 'category_id',
            'brand', 'brand_id',
            'images', 'variants',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']