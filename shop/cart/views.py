from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product

from .models import Cart, CartItem
from products.forms import QuantityForm


def add_to_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)

    # Základní hodnota quantity
    quantity = int(quantity)  # Ujistěte se, že quantity je int

    if request.method == 'POST':
        form = QuantityForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
        else:
            messages.error(request, 'Neplatná hodnota')
            return redirect('product_detail', product_id=product.id)  # Přesměrování na detail produktu

    if quantity < 1:
        quantity = 1

    if quantity > product.stock:
        messages.error(request, 'Není dostatek zboží na skladě.')
        return redirect('product_detail', product_id=product.id)

    # Přidání do košíku
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    # Uložení
    cart_item.save()

    # Odečti sklad
    product.stock -= quantity
    product.save()

    context = {
        'product': product
    }

    messages.success(request, 'Zboží bylo úspěšně přidáno do košíku!')
    return render(request, 'cart_confirmation.html', context)  # Odkaz na potvrzení


def remove_from_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)

    # Základní hodnota quantity
    quantity = int(quantity)  # Ujistěte se, že quantity je int

    if request.method == 'POST':
        form = QuantityForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
        else:
            messages.error(request, 'Neplatná hodnota')
            return redirect('product_detail', product_id=product.id)  # Přesměrování na detail produktu

    if quantity < 1:
        quantity = 1

    if quantity > product.stock:
        messages.error(request, 'Není dostatek zboží na skladě.')
        return redirect('product_detail', product_id=product.id)

    # Přidání do košíku

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    # Uložení
    cart_item.save()

    # Odečti sklad
    product.stock -= quantity
    product.save()

    context = {
        'product': product
    }

    messages.success(request, 'Zboží bylo úspěšně přidáno do košíku!')
    return render(request, 'cart_confirmation.html', context)  # Odkaz na potvrzení


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.get_user_cart_items(request.session, request.user)
    else:
        cart_items = request.session.get('cart', {})

    products = []

    for item in cart_items:
        product = get_object_or_404(Product, id=item.product.id)
        products.append({'product': product, 'quantity': item.quantity})

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': products,
        'total_price': total_price
    })
