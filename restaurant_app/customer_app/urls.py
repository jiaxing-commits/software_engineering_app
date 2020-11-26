from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.default_home, name='default_home'),
    path('logged', views.logged_home, name='logged_home'),
    path('menu', views.menu, name='menu'),
    path('checkout', views.checkout, name='checkout'),
    path('customer_account_creation_form', views.customer_account_creation_form, name='customer_account_creation_form'),
]