from django.shortcuts import render, redirect

# Create your views here.

user = ''

def employee_portal(request):
    if request.session['Logged_Status'] != 'LOGGED':
        return redirect('../login')
    else:
        if 'User' in request.session:
            user = request.session['User']
        return render(request, 'staff_app/employee_portal.html')