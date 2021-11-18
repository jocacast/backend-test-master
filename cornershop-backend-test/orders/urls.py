from django.urls import path, include
from . import views
urlpatterns = [
    path('create_order/<str:pk>', views.createOrder, name='create_order'),
    path('my_orders/' , views.myOrders, name='my_orders'),
    path('all_orders/', views.allOrders, name='all_orders')
]