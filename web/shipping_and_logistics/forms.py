from django import forms
from .models import ShippingAddress, OrderTracking, ShippingProvider

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }

class OrderTrackingForm(forms.ModelForm):
    class Meta:
        model = OrderTracking
        fields = ['order', 'shipping_address', 'shipping_provider', 'status', 'tracking_number']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'tracking_number': forms.TextInput(attrs={'placeholder': 'Enter Tracking Number'}),
        }

class ShippingProviderForm(forms.ModelForm):
    class Meta:
        model = ShippingProvider
        fields = ['name', 'contact_number', 'website']
        widgets = {
            'website': forms.URLInput(attrs={'placeholder': 'https://'}),
        }
