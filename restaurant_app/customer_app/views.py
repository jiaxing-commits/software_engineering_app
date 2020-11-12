from django.shortcuts import render

def default_home(request):
    return render(request, 'customer_app/default_home.html')

def logged_home(request):
    return render(request, 'customer_app/logged_home.html')

def menu(request):
    return render(request, 'customer_app/menu.html')

def checkout(request):
    return render(request, 'customer_app/checkout.html')

def customer_portal(request):
    return render(request, 'customer_app/customer_portal.html')