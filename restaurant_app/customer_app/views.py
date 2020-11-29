from django.shortcuts import render, redirect
from db_models.models import Current_Orders, Customer, Order_history, Staff
from db_models.forms import CustomerForm
from collections import defaultdict

user = 'guest'
cart = defaultdict()

def default_home(request):
    if 'Logged_Status' in request.session.keys() and request.session['Logged_Status'] != 'LOGGED':
        return render(request, 'customer_app/default_home.html')
    else:
        return redirect('logged')

def logged_home(request):
    if 'Logged_Status' in request.session.keys() and request.session['Logged_Status'] != 'LOGGED':
        return redirect('login')
    else:
        if 'User' in request.session:
            user = request.session['User']
        return render(request, 'customer_app/logged_home.html')

def menu(request):
    if request.method == 'POST':
        if request.POST.get('item'):
            cart[request.POST.get('item')] = request.POST.get('quanity')
        
        request.POST = request.POST.copy()
        context = {'cart': cart}
    return render(request, 'customer_app/menu.html', context)

def checkout(request):
    return render(request, 'customer_app/checkout.html')

def customer_account_creation_form(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            #check if 2nd password is correct
        
            if request.POST['password'] == request.POST['re_enter_password']:
                customer_form.save()
                return redirect('..')
            else:
                context = {'customer_form': customer_form, 'email_valid': True, 'password_valid': False}
            return render(request, 'customer_app/customer_account_creation_form.html', context)
        else: 
            if Customer.objects.filter(email=request.POST['email']).exists():
                context = {'customer_form': customer_form, 'email_valid': False, 'password_valid': True}
            return render(request, 'customer_app/customer_account_creation_form.html', context)
    customer_form = CustomerForm()
    context = {'customer_form': customer_form, 'email_valid': True, 'password_valid': True}
    return render(request, 'customer_app/customer_account_creation_form.html', context)

def order_history(request):
    if request.session['Logged_Status'] != 'LOGGED':
        return redirect('login')
    else:
        if 'User' in request.session:
            user = request.session['User']  
        total_orders = Order_history.objects.all()
        current_user = []
        for i in total_orders: 
            customer = Customer.objects.get(customer_id = i.customer_id) 
            current_user.append(customer.customer_id)
        total_orders = [[x,y] for (x,y) in zip(total_orders, current_user)]
        context = { 'total_orders': total_orders }


        return render(request, 'customer_app/order_history.html', context)