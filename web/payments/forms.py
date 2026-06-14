from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'transaction_id']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Optional for COD'}),
        }

    def clean_transaction_id(self):
        transaction_id = self.cleaned_data.get('transaction_id')
        payment_method = self.cleaned_data.get('payment_method')

        if payment_method == 'Card' and not transaction_id:
            raise forms.ValidationError("Transaction ID is required for Card payments.")
        return transaction_id
