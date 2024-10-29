from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404

from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_user_cart_items(session, user):
        cart = Cart.objects.filter(user=user).first()
        if cart is None:
            # Přenos položek z session do databáze
            cart = Cart()
            cart.user = user
            cart.save()
            session_cart = session.get('cart', {})
            if session_cart:
                cart, created = Cart.objects.get_or_create(user=user)

                for product_id, quantity in session_cart.items():
                    product = get_object_or_404(Product, id=product_id)
                    CartItem.objects.create(cart=cart, product=product, quantity=quantity)

                # Po úspěšném přenosu položek vyprázdni session
                session['cart'] = {}

        return cart.items.all()  # Získání všech položek v košíku


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
