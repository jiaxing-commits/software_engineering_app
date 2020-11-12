from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.default_home, name='default_home'),
    path('logged', views.logged_home, name='logged_home'),
    path('menu', views.menu, name='menu'),
    path('checkout', views.checkout, name='checkout'),
    path('customer_portal', views.customer_portal, name='customer_portal'),
]