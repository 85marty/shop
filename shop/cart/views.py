from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from products.forms import QuantityForm
from products.models import Product

from .models import Cart, CartItem


def add_to_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)

    # Základní hodnota quantity
    quantity = int(quantity)  # Ujistit se, že quantity je int

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
    if request.user.is_authenticated:  # Uložení do DB
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
    else:  # Uložení do session
        cart_items = request.session.get('cart_items', [])
        found = False
        for item in cart_items:
            if item['product_id'] == product.id:
                item['quantity'] += quantity
                found = True
                break
        if not found:
            cart_items.append({'product_id': product.id, 'quantity': quantity})
        # Uložení aktualizovaného seznamu do session
        request.session['cart_items'] = cart_items

    # Odečti sklad
    product.stock -= quantity
    product.save()

    context = {
        'product': product,
        'action': 'added',
    }

    messages.success(request, 'Zboží bylo úspěšně přidáno do košíku!')
    return render(request, 'cart_confirmation.html', context)  # Odkaz na potvrzení


def remove_from_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)

    # Základní hodnota quantity
    quantity = int(quantity)  # Ujistit se, že quantity je int

    if request.method == 'POST':
        form = QuantityForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
        else:
            messages.error(request, 'Neplatná hodnota')
            return redirect('product_detail', product_id=product.id)  # Přesměrování na detail produktu

    if quantity < 1:
        quantity = 1

    # Odebrání z košíku
    if request.user.is_authenticated:  # Uložení do DB
        cart, created = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})

        if cart_item.quantity > quantity:
            cart_item.quantity -= quantity
            cart_item.save()
        else:
            cart_item.delete()
    else:  # Uložení do session
        cart_items = request.session.get('cart_items', [])
        for index, item in enumerate(cart_items):
            if item['product_id'] == product.id:
                if item['quantity'] > quantity:
                    item['quantity'] -= quantity
                else:
                    del cart_items[index]
                break
        # Uložení aktualizovaného seznamu do session
        request.session['cart_items'] = cart_items

    # Vrať na sklad
    product.stock += quantity
    product.save()

    context = {
        'product': product,
        'action': 'removed',
    }

    messages.success(request, 'Zboží bylo odebráno z košíku!')
    return render(request, 'cart_confirmation.html', context)  # Odkaz na potvrzení


def cart_view(request):
    products = []
    total_price = 0

    if request.user.is_authenticated:
        # Načtení položek z databáze
        cart_items = Cart.get_user_cart_items(request.session, request.user)
        for item in cart_items:
            product = item.product
            quantity = item.quantity
            products.append({'product': product, 'quantity': quantity})
            total_price += product.price * quantity
    else:
        # Načtení položek ze session
        cart_items = request.session.get('cart_items', [])
        for item in cart_items:
            product = get_object_or_404(Product, id=item['product_id'])
            quantity = item['quantity']
            products.append({'product': product, 'quantity': quantity})
            total_price += product.price * quantity

    return render(request, 'cart.html', {
        'cart_items': products,
        'total_price': total_price
    })
