from django.shortcuts import render, redirect
from db_models.models import Customer, Staff

def login(request):

    if request.method == 'GET':
        # c = Customer(email='aushdaisudhiashdaisudhiau@gmail.com', phone='123',password='asdasd')
        # s = Staff(email='naan@gmail.com', password='asdasd')
        # c.save()
        # s.save()
        
        if 'username' in request.GET and 'password' in request.GET:
            #if customer logs in
            if Customer.objects.filter(email=request.GET['username'], password=request.GET['password']).exists():
                request.session['User'] = request.GET['username']
                request.session['Logged_Status'] = 'LOGGED'
                return redirect('/../logged')
            
            #if staff logs in
            if Staff.objects.filter(email=request.GET['username'], password=request.GET['password']).exists():
                request.session['User'] = request.GET['username']
                request.session['Logged_Status'] = 'LOGGED'
                return redirect('/../employee_portal')

    return render(request, 'login_app/login.html')

def log_out(request):
    request.session['User'] = ''
    request.session['Role'] = ''
    request.session['Logged_Status'] = 'NOT LOGGED'
    return redirect('..')