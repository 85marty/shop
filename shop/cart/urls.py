from django.urls import path

from .views import cart_view, add_to_cart

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/<int:quantity>/', add_to_cart, name='add_to_cart'),
]
