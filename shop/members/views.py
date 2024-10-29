from cart.models import Cart, CartItem
from core.helpers import group_required_decorator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic
from members.models import Member
from members.models import create_member_for_user
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
            session_cart = request.session.get('cart_items', {})
            if session_cart:
                cart, created = Cart.objects.get_or_create(user=user)

                for item in session_cart:
                    product_id = item['product_id']
                    quantity = item['quantity']
                    product = get_object_or_404(Product, id=product_id)
                    CartItem.objects.create(cart=cart, product=product, quantity=quantity)

                # Po úspěšném přenosu položek vyprázdni session
                request.session['cart_items'] = {}

            next_url = request.POST.get('next') or 'product_list'
            next_url = 'product_list'
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


# jen admin
@method_decorator(group_required_decorator('shop_admin'), name='dispatch')
class MemberListView(generic.ListView):
    model = User
    template_name = 'member_list.html'
    context_object_name = 'members'  # Kontext pro šablonu


# Detail uživatele
class MemberDetailView(LoginRequiredMixin, generic.DetailView):
    model = Member
    template_name = 'member_detail.html'
    context_object_name = 'member'

    def get_object(self, queryset=None):
        user = self.request.user
        member, created = Member.objects.get_or_create(user=user)

        return member


# Editace uživatele
class MemberUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Member
    fields = ['address', 'phone_number']  # Pole přímo z modelu Member
    template_name = 'member_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('member_detail', kwargs={'pk': self.object.pk})

    def get_object(self):
        # Získání uživatelského objektu
        user = self.request.user

        # Získání člena
        try:
            return user.member
        except Member.DoesNotExist:
            return create_member_for_user(user)
        return self.request.user.member  # Zajišťuje, že uživatel upravuje svůj vlastní profil

    def form_valid(self, form):
        # Uložíme data do Member
        response = super().form_valid(form)

        # Uložíme data do User
        user = self.request.user
        user.first_name = self.request.POST.get('first_name')
        user.last_name = self.request.POST.get('last_name')
        user.email = self.request.POST.get('email')
        user.save()

        return response


# jen admin
@method_decorator(group_required_decorator('shop_admin'), name='dispatch')
class MemberDeleteView(generic.DeleteView):
    model = User
    template_name = 'member_confirm_delete.html'
    success_url = reverse_lazy('member_list')

    def get_queryset(self):
        return User.objects.all()
