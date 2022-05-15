from django.urls import path, include
from . import views

urlpatterns = [
    path('employee_portal/', views.employee_portal, name='employee_portal'),
]