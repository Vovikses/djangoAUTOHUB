from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('success/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
]