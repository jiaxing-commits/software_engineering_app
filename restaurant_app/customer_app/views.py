from django.shortcuts import render, redirect
from db_models.models import Customer
from db_models.forms import CustomerForm

user = ''

def default_home(request):
    if request.session['Logged_Status'] != 'LOGGED':
        return render(request, 'customer_app/default_home.html')
    else:
        return redirect('../logged')

def logged_home(request):
    if request.session['Logged_Status'] != 'LOGGED':
        return redirect('../login')
    else:
        if 'User' in request.session:
            user = request.session['User']
        return render(request, 'customer_app/logged_home.html')

def menu(request):
    return render(request, 'customer_app/menu.html')

def checkout(request):
    return render(request, 'customer_app/checkout.html')

def customer_account_creation_form(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            
        else:
            print(customer_form.errors)
    customer_form = CustomerForm()
    context = {'customer_form': customer_form}
    return render(request, 'customer_app/customer_account_creation_form.html', context)