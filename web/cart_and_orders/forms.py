from django import forms
from .models import CartItem, Order
from product_management.models import ProductVariant

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['variant', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['variant'].queryset = ProductVariant.objects.all()
        self.fields['variant'].required = False
        self.fields['variant'].empty_label = "No variant"

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'billing_address']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholder text for user guidance
        self.fields['shipping_address'].widget.attrs.update({'placeholder': 'Enter shipping address'})
        self.fields['billing_address'].widget.attrs.update({'placeholder': 'Enter billing address'})
