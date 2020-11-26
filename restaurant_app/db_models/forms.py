from django import forms


from .models import *

class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'street', 'city', 'state', 'postal_code', 'phone', 'email', 'password', 'name_on_card', 'credit_card_number', 'cvv_number', 'billing_street', 'billing_city', 'billing_state', 'billing_postal_code')

###
customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=26)
    last_name = models.CharField(max_length=26)
    street = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    postal_code = models.CharField(max_length=5) #check
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=320)
    password = models.CharField(max_length=50)

    #Card Information
    name_on_card = models.CharField(max_length=30)
    credit_card_number = models.CharField(max_length=16) #check
    cvv_number = models.CharField(max_length=3) #check
    billing_street = models.CharField(max_length=35)
    billing_city = models.CharField(max_length=35)
    billing_state = models.CharField(max_length=35)
    billing_postal_code = models.CharField(max_length=5) #check

###