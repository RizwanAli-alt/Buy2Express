from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product, Category, Seller, Brand,
    ProductImage, ProductSpecification, ProductVariant,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    @admin.display(description='Preview')
    def preview(self, obj):
        if getattr(obj, 'image', None):
            return format_html(
                '<img src="{}" style="height:50px; border-radius:6px;">', obj.image.url
            )
        return '—'


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail', 'name', 'category', 'seller', 'price',
        'stock_badge', 'is_active', 'is_featured', 'created_at',
    )
    list_display_links = ('name',)
    list_editable = ('is_active', 'is_featured')
    list_filter = ('category', 'brand', 'is_active', 'is_featured', 'seller')
    search_fields = ('name', 'description', 'seller__name')
    autocomplete_fields = ('seller', 'category', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    list_select_related = ('category', 'seller', 'brand')
    list_per_page = 25
    save_on_top = True
    inlines = [ProductImageInline, ProductVariantInline, ProductSpecificationInline]
    actions = ('feature_products', 'unfeature_products', 'activate_products', 'deactivate_products')

    LOW_STOCK_THRESHOLD = 10

    # Falls back to the default reverse accessor (productimage_set) if you
    # haven't set related_name='images' on the ProductImage FK.
    @admin.display(description='Image')
    def thumbnail(self, obj):
        first_image = obj.images.first() if hasattr(obj, 'images') else obj.productimage_set.first()
        if first_image and getattr(first_image, 'image', None):
            return format_html(
                '<img src="{}" style="height:42px; width:42px; object-fit:cover; '
                'border-radius:8px;">', first_image.image.url
            )
        return format_html('<span style="color:#999;">No image</span>')

    @admin.display(description='Stock')
    def stock_badge(self, obj):
        if obj.stock <= 0:
            color, label = '#E24B4A', 'Out of stock'
        elif obj.stock <= self.LOW_STOCK_THRESHOLD:
            color, label = '#F5A623', f'Low ({obj.stock})'
        else:
            color, label = '#2E7D32', f'{obj.stock} in stock'
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:700;">{}</span>',
            color, label,
        )

    @admin.action(description='Mark selected products as featured')
    def feature_products(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} product(s) marked as featured.')

    @admin.action(description='Remove selected products from featured')
    def unfeature_products(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} product(s) removed from featured.')

    @admin.action(description='Activate selected products')
    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} product(s) activated.')

    @admin.action(description='Deactivate selected products')
    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} product(s) deactivated.')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'product_count', 'description')
    list_filter = ('parent_category',)
    search_fields = ('name',)
    autocomplete_fields = ('parent_category',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 30

    @admin.display(description='Products')
    def product_count(self, obj):
        return obj.product_set.count()


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating_stars', 'is_verified', 'product_count')
    list_editable = ('is_verified',)
    list_filter = ('is_verified',)
    search_fields = ('name', 'email')
    list_per_page = 30
    actions = ('verify_sellers', 'unverify_sellers')

    @admin.display(description='Rating')
    def rating_stars(self, obj):
        try:
            full = max(0, min(5, int(round(obj.rating))))
        except (TypeError, ValueError):
            full = 0
        return '★' * full + '☆' * (5 - full)

    @admin.display(description='Products')
    def product_count(self, obj):
        return obj.product_set.count()

    @admin.action(description='Verify selected sellers')
    def verify_sellers(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} seller(s) verified.')

    @admin.action(description='Unverify selected sellers')
    def unverify_sellers(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} seller(s) unverified.')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    list_per_page = 30

    @admin.display(description='Products')
    def product_count(self, obj):
        return obj.product_set.count()


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'preview')
    search_fields = ('product__name',)
    autocomplete_fields = ('product',)
    list_select_related = ('product',)
    list_per_page = 40

    @admin.display(description='Preview')
    def preview(self, obj):
        if getattr(obj, 'image', None):
            return format_html('<img src="{}" style="height:46px; border-radius:6px;">', obj.image.url)
        return '—'


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')
    list_editable = ('value',)
    search_fields = ('product__name', 'key')
    autocomplete_fields = ('product',)
    list_select_related = ('product',)
    list_per_page = 40


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name')
    search_fields = ('product__name', 'name')
    autocomplete_fields = ('product',)
    list_select_related = ('product',)
    list_per_page = 40