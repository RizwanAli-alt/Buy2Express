from django import forms
from django.forms import inlineformset_factory
from .models import (
    Product,
    Category,
    Brand,
    ProductImage,
    ProductSpecification,
    ProductVariant
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'brand', 'seller',
            'description', 'price', 'discount_price',
            'stock', 'is_active', 'is_featured'
        ]
        widgets = {
            'slug': forms.TextInput(
                attrs={'placeholder': 'Auto-generated from name if left blank'}
            ),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']


class ProductSpecificationForm(forms.ModelForm):
    class Meta:
        model = ProductSpecification
        fields = ['product', 'key', 'value']


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'name', 'options']
        widgets = {
            'options': forms.TextInput(
                attrs={'placeholder': 'Comma-separated values, e.g., S,M,L'}
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent_category', 'description', 'image']
        widgets = {
            'slug': forms.TextInput(
                attrs={'placeholder': 'Auto-generated from name if left blank'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo'].required = True


# Multiple Product Images FormSet
ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    fields=['image'],
    extra=1,          # 1 image upload field by default
    can_delete=True
)