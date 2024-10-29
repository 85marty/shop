from cart.models import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from orders.models import Order, OrderItem

from core.helpers import group_required


@login_required
def order_success(request):
    return render(request, 'order_success.html')


@login_required
def create_order(request):
    if request.user.is_authenticated:
        cart_items = Cart.get_user_cart_items(request.session, request.user)
    else:
        cart_items = request.session.get('cart', {})

    if not cart_items:
        return redirect('cart')  # Pokud je košík prázdný

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(user=request.user, total_amount=total_amount, status='new')

    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)

    # Po vytvoření objednávky vyprázdni košík
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()
    else:
        request.session['cart'] = {}

    return redirect('order_success')  # Přesměrování na stránku s potvrzenímfrom django.shortcuts import render


# @login_required
# def order_list(request):
#     orders = Order.objects.filter(user=request.user)
#     return render(request, 'order_list.html', {'orders': orders})


@login_required
def order_list(request):
    all_param = request.GET.get('all', 'false')
    if all_param and group_required('shop_admin', request):
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    return render(request, 'order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, 'Stav objednávky byl úspěšně změněn.')

    return render(request, 'order_detail.html', {'order': order})
