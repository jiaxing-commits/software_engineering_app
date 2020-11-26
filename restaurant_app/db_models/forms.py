from django import forms


from .models import *

class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'street', 'city', 'state', 'postal_code', 'phone', 'email', 'password', 'name_on_card', 'credit_card_number', 'cvv_number', 'billing_street', 'billing_city', 'billing_state', 'billing_postal_code')
