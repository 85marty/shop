from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import ProductForm, CategoryForm, QuantityForm
from .models import Product, Category
from core.helpers import group_required_decorator


# všichni
class ProductListView(generic.ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        # Zavolání rodičovské metody, abychom získali základní kontext
        context = super().get_context_data(**kwargs)
        # Přidání seznamu kategorií do kontextu
        context['categories'] = Category.objects.all()

        return context

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            return Product.objects.filter(category__slug=category_slug)
        return Product.objects.all()


# všichni
class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuantityForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Přesměrování na pohled pro přidání do košíku
            return redirect('add_to_cart', product_id=self.object.id, quantity=quantity)
        return self.get(request, *args, **kwargs)


# jen admin
@method_decorator(group_required_decorator('shop_admin'), name='dispatch')
class ProductDeleteView(generic.DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Product.objects.all()


# jen admin
@method_decorator(group_required_decorator('shop_admin'), name='dispatch')
class ProductCreateView(generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = '/products/'


# jen admin
@method_decorator(group_required_decorator('shop_admin'), name='dispatch')
class ProductUpdateView(generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = '/products/'


# jen admin
@method_decorator(group_required_decorator('shop_admin'), name='dispatch')
class CategoryDeleteView(generic.DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Category.objects.all()


# jen admin
@method_decorator(group_required_decorator('shop_admin'), name='dispatch')
class CategoryCreateView(generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = '/products/'


# jen admin
@method_decorator(group_required_decorator('shop_admin'), name='dispatch')
class CategoryUpdateView(generic.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = '/products/'
