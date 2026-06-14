from django import forms
from .models import Wishlist, FavoriteStore

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product']

class FavoriteStoreForm(forms.ModelForm):
    class Meta:
        model = FavoriteStore
        fields = ['seller']
