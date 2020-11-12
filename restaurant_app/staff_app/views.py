from django.shortcuts import render

# Create your views here.

def employee_portal(request):
    return render(request, 'staff_app/employee_portal.html')