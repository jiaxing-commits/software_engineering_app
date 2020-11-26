from django.shortcuts import render
from db_models.models import Customer

def default_home(request):
    return render(request, 'customer_app/default_home.html')

def logged_home(request):
    return render(request, 'customer_app/logged_home.html')

def menu(request):
    return render(request, 'customer_app/menu.html')

def checkout(request):
    return render(request, 'customer_app/checkout.html')

def customer_account_creation_form(request):
    if request.method == 'POST':
        c = Customer(first_name = request.GET['first_name'], 
        last_name = request.GET['last_name'],
        street = request.GET['street'], 
        city = request.GET['city'], 
        state = request.GET['state'], 
        postal_code = request.GET['postal_code'], 
        email = request.GET['email'], 
        phone = request.GET['phone'], 
        name_on_card = request.GET['name_on_card'], 
        credit_card_number = request.GET['credit_card_number'], 
        cvv_number = request.GET['cvv_number'])
        )
        c.save()

        #print(request.GET.get('first_name'))
    return render(request, 'customer_app/customer_account_creation_form.html')