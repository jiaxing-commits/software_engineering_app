from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.login, name='login'),
    path('employee_portal', views.employee_portal, name='employee_portal'),
]