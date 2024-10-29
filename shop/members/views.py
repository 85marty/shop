from functools import wraps

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from members.models import Member

from cart.models import Cart, CartItem
from products.models import Product


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Přenos položek z session do databáze
            session_cart = request.session.get('cart', {})
            if session_cart:
                cart, created = Cart.objects.get_or_create(user=user)

                for product_id, quantity in session_cart.items():
                    product = get_object_or_404(Product, id=product_id)
                    CartItem.objects.create(cart=cart, product=product, quantity=quantity)

                # Po úspěšném přenosu položek vyprázdni session
                request.session['cart'] = {}

            next_url = request.POST.get('next', 'home')  # výchozí hodnota je 'home'
            return redirect(next_url)
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    if request.method == 'GET':
        next_url = request.GET.get('next', 'home')  # výchozí hodnota je 'home'
        return redirect(next_url)
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)

        Member.objects.create(user=user)

        return redirect('login')

    return render(request, 'register.html', )


# Seznam uživatelů
class MemberListView(generic.ListView):
    model = User
    template_name = 'member_list.html'
    context_object_name = 'members'  # Kontext pro šablonu


# Detail uživatele
class MemberDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'member_detail.html'
    context_object_name = 'member'


# Editace uživatele
class MemberUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']  # Atributy, které může uživatel měnit
    template_name = 'member_form.html'
    success_url = reverse_lazy('member_list')

    def get_object(self):
        return self.request.user  # Zajišťuje, že uživatel upravuje svůj vlastní profil
