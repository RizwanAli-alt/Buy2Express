from django import forms
from .models import SearchQuery

class SearchQueryForm(forms.ModelForm):
    class Meta:
        model = SearchQuery
        fields = ['query'] 