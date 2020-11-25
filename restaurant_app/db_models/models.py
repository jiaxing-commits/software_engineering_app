from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Customer(models.Model):
    # remember checks for constrict in the input form with postal code, credit card number, CVV
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=26)
    last_name = models.CharField(max_length=26)
    street = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    email = models.EmailField(max_length=320)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    postal_code = models.CharField(max_length=5) #check
    name_on_card = models.CharField(max_length=30)
    credit_card_number = models.CharField(max_length=16) #check
    cvv_number = models.CharField(max_length=3) #check
    total_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ,ID: ' + str(self.customer_id)