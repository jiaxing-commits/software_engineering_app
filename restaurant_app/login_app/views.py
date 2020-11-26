from django.shortcuts import render, redirect
from db_models.models import Customer, Staff

def login(request):

    if request.method == 'GET':
        if 'username' in request.GET and 'password' in request.GET:
            if Customer.objects.filter(email=request.GET['username'], password=request.GET['password']).exists():
                return redirect('/../logged')
        return render(request, 'login_app/login.html')


    return render(request, 'login_app/login.html')