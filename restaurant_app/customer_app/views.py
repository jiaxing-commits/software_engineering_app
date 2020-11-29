from django.shortcuts import render, redirect
from db_models.models import Current_Orders, Customer, Order_history, Staff, Menu
from db_models.forms import CustomerForm
from collections import defaultdict
from decimal import Decimal
import json

cart = defaultdict()

def default_home(request):
    if 'Logged_Status' in request.session.keys() and request.session['Logged_Status'] != 'LOGGED':
        return render(request, 'customer_app/default_home.html')
    else:
        return redirect(logged_home)

def logged_home(request):
    if 'Logged_Status' in request.session.keys() and request.session['Logged_Status'] != 'LOGGED':
        return redirect('login')
    else:
        total_price = 0
        total_quanity = 0
        for x, y in cart.items():
            total_price += y[1]
            total_quanity += int(y[0])
            
        user = request.session['User']
        context = {'cart': cart, 'total_price': total_price, 'total_quanity': total_quanity, 'user': user}
        return render(request, 'customer_app/logged_home.html', context)

def menu(request):
    if request.method == 'POST':
        if request.POST.get('item'):
            total_per_item = Decimal(request.POST.get('quanity'))*Decimal(Menu.objects.get(item_name=request.POST.get('item')).price)
            cart[request.POST.get('item')] = [request.POST.get('quanity'), total_per_item]
    
    context = {'cart': cart}
    return render(request, 'customer_app/menu.html', context)

def checkout(request):
    user = request.session['User']
    total_price = 0
    total_quanity = 0

    print(user)

    if request.method == 'POST':
        if request.POST.get('Confirm Payment'):
            item_list = {}
            
            for x,y in cart.items():
                item_list[x] = int(y[0])
                total_price += y[1]
            item_list =  json.dumps(item_list)
            
            if user:
                c = Current_Orders(customer_id=Customer.objects.get(email=user).customer_id, item_list = item_list, total_price=total_price)
                c.save()
                return redirect(logged_home)
            else:
                c = Current_Orders(customer_id=-1, item_list = item_list, total_price=total_price)
                c.save()
                return redirect(default_home)
    total_price = 0
    total_quanity = 0
    for x, y in cart.items():
        total_price += y[1]
        total_quanity += int(y[0])

    context = {'cart': cart, 'total_price': total_price, 'total_quanity': total_quanity, 'user': user}
    return render(request, 'customer_app/checkout.html', context)

def customer_account_creation_form(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            #check if 2nd password is correct
        
            if request.POST['password'] == request.POST['re_enter_password']:
                customer_form.save()
                return redirect(default_home)
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