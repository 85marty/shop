from django.urls import path

from .views import create_order, order_success, order_list, order_detail

urlpatterns = [
    path('order_list/', order_list, name='order_list'),
    path('<int:order_id>/', order_detail, name='order_detail'),
    path('create-order/', create_order, name='create_order'),
    path('order-success/', order_success, name='order_success'),
]
