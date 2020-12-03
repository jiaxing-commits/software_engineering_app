from django.shortcuts import render, redirect
from db_models.models import Current_Orders, Customer, Order_history, Staff, Menu
from db_models.forms import CustomerForm
from collections import defaultdict
from decimal import Decimal
import json

cart = defaultdict()

def default_home(request):
    if 'Logged_Status' in request.session.keys() and request.session['Logged_Status'] == 'LOGGED':
        return redirect(logged_home)
    else:
        if request.method == 'POST':
            if request.POST.get('item'):
                total_per_item = Decimal(request.POST.get('quanity'))*Decimal(Menu.objects.get(item_name=request.POST.get('item')).price)
                cart[request.POST.get('item')] = [request.POST.get('quanity'), total_per_item]

            if request.POST.get('delete_item'):
                del cart[request.POST.get('delete_item')]
        
        total_price = 0

        for x, y in cart.items():
            total_price += y[1]

        context2 = {'cart': cart, 'total_price': total_price}
        return render(request, 'customer_app/default_home.html', context2)

def logged_home(request):
    if 'Logged_Status' in request.session.keys() and request.session['Logged_Status'] == 'LOGGED':
        if request.method == 'POST':
            if request.POST.get('item'):
                total_per_item = Decimal(request.POST.get('quanity'))*Decimal(Menu.objects.get(item_name=request.POST.get('item')).price)
                cart[request.POST.get('item')] = [request.POST.get('quanity'), total_per_item]

            if request.POST.get('delete_item'):
                del cart[request.POST.get('delete_item')]

        total_price = 0

        for x, y in cart.items():
            total_price += y[1]

        context = {'cart': cart, 'total_price': total_price}

        return render(request, 'customer_app/logged_home.html', context)
    else:
        return redirect('login')
        

def menu(request):
    if request.method == 'POST':
        if request.POST.get('item'):
            total_per_item = Decimal(request.POST.get('quanity'))*Decimal(Menu.objects.get(item_name=request.POST.get('item')).price)
            cart[request.POST.get('item')] = [request.POST.get('quanity'), total_per_item]
        if request.POST.get('delete_item'):
            print("sdfdsfsdf")
            del cart[request.POST.get('delete_item')]
    
    total_price = 0

    for x, y in cart.items():
        total_price += y[1]
    
    context = {'cart': cart, 'total_price':total_price}
    return render(request, 'customer_app/menu.html', context)

def checkout(request):
    user = request.session['User'] if 'User' in request.session else None
    total_price = 0
    total_quanity = 0

    if request.method == 'POST':
        if request.POST.get('Confirm Payment'):
            item_list = {}
            
            for x,y in cart.items():
                item_list[x] = int(y[0])
                total_price += y[1]
            item_list =  json.dumps(item_list)
            
            acc_points = int(total_price) * 2

            if user and len(cart) != 0:
                customer = Customer.objects.get(email=user)
                customer.total_points += acc_points
                customer.save()

                c = Current_Orders(customer_id=customer.customer_id, item_list = item_list, total_price=total_price)
                c.save()
                cart.clear()
                return redirect(logged_home)
            elif len(cart) != 0:
                c = Current_Orders(customer_id=-1, item_list = item_list, total_price=total_price)
                c.save()
                cart.clear()
                return redirect(default_home)
        
        if request.POST.get('Use Points'):
            customer = Customer.objects.get(email=user)
            points_to_money = 0

            if customer.total_points >= 100:
                points_to_money = customer.total_points // 100
                customer.total_points = customer.total_points % 100 
                customer.save()
                total_price -= points_to_money

    for x, y in cart.items():
        total_price += y[1]
        total_quanity += int(y[0])
    
    if user:
        cur_points = Customer.objects.get(email=user).total_points
        context = {'cart': cart, 'total_price': total_price, 'total_quanity': total_quanity, 'user': user, 'cur_points': cur_points}
    else:
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
        total_orders = Order_history.objects.all()
        current_user = []
        for i in total_orders: 
            customer = Customer.objects.get(customer_id = i.customer_id) 
            current_user.append(customer.customer_id)
        total_orders = [[x,y] for (x,y) in zip(total_orders, current_user)]
        context = { 'total_orders': total_orders }


        return render(request, 'customer_app/order_history.html', context)