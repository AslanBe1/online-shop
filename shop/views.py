from typing import Optional
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from shop.models import Product, Category, Order, Comment
from shop.forms import OrderForm, CommentModelForm, ProductModelForm, OrderModelForm


# Create your views here.

def index(request, category_id: Optional[int] = None):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')
    categorys = Category.objects.all()
    if category_id:
        if filter_type == 'expensive':
            products = Product.objects.filter(category_id=category_id).order_by('-price')
        elif filter_type == 'cheap':
            products = Product.objects.filter(category_id=category_id).order_by('price')
        elif filter_type == 'rating':
            products = Product.objects.filter(category_id=category_id, rating__gte=4).order_by('-rating')

        else:
            products = Product.objects.filter(category_id=category_id)


    else:
        if filter_type == 'expensive':
            products = Product.objects.filter().order_by('-price')
        elif filter_type == 'cheap':
            products = Product.objects.filter().order_by('price')
        elif filter_type == 'rating':
            products = Product.objects.filter(rating__gte=4).order_by('-rating')

        else:
            products = Product.objects.all()


    if search_query:
        products = Product.objects.filter(name__icontains=search_query)

    context = {'products': products,
               'categorys': categorys,
    }
    return render(request, 'shop/index.html', context)


# def product_detail(request,pk):
#     products = get_object_or_404(Product, pk=pk)
#     comments = Comment.objects.filter(product=products, is_negative=False)
#     related_products = Product.objects.filter(category_id=products.category_id).exclude(id=products.id)
#
#     context = {'products': products,
#                'comments': comments,
#                'related_products': related_products,
#                }
#
#     return render(request,'shop/detail.html',context=context)


# def order_detail(request,pk):
#     products = get_object_or_404(Product, id=pk)
#     if request.method == 'GET':
#         form = OrderForm(request.GET)
#         if form.is_valid():
#             full_name = request.GET.get('full_name')
#             phone_number = request.GET.get('phone_number')
#             quantity = int(request.GET.get('quantity'))
#
#             if products.quantity >= quantity:
#                 products.quantity = products.quantity - quantity
#                 order = Order.objects.create(full_name=full_name,
#                                              phone_number=phone_number,
#                                              quantity=quantity,
#                                              product=products)
#                 products.save()
#                 order.save()
#                 messages.add_message(request, messages.SUCCESS,'Your order has been added Successfully!.')
#             else:
#                 messages.add_message(request, messages.ERROR,'Quantity is raise full\'s')
#     else:
#         form = OrderForm()
#
#     context = {'form': form,
#                    'products': products,}
#     return render(request, 'shop/detail.html', context)

#
# def comment_detail(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     form = CommentModelForm()
#     if request.method == 'POST':
#         form = CommentModelForm(request.POST)
#
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.product = product
#             comment.save()
#             return redirect('product_detail', pk)
#     context = {
#         'product': product,
#         'form': form
#     }
#     return render(request, 'shop/detail.html', context=context)
#
#
#
def about(request):
    return render(request,'shop/index2.html')

# @login_required
# def create_product(request):
#     form =  ProductModelForm()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('apelsin')
#     else:
#         form = ProductModelForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'shop/Create.html', context)

@login_required
def delete_product(request, pk):
    try:
        products = get_object_or_404(Product, id=pk)
        products.delete()
        return redirect('apelsin')

    except Product.DoesNotExist as e:
        print(e)


# @login_required
# def edit_product(request, pk):
#     products = get_object_or_404(Product, id=pk)
#     form = ProductModelForm(instance=products)
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES, instance=products)
#         if form.is_valid():
#             form.save()
#             return redirect('product_detail', pk)
#
#     context = {
#          'form': form,
#          'products': products,
#      }
#
#     return render(request, 'shop/edit.html' , context=context)
#


class CreateProductView(CreateView):
    model = Product
    template_name = 'shop/create.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('apelsin')


class EditProductView(UpdateView):
    model = Product
    template_name = 'shop/edit.html'
    form_class = ProductModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.kwargs['pk']})


class CommentCreateView(CreateView):
    def get(self, request, **kwargs):
        form = CommentModelForm()
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        return render(request, 'shop/index.html', {'form': form,'product':product})

    def post(self, request, **kwargs):
        form = CommentModelForm(request.POST)
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', pk=product.id)

        return render(request, 'shop/index.html', {'form': form,'product':product})


class OrderCreateView(CreateView):
    def get(self, request, **kwargs):
        products = get_object_or_404(Product, id=self.kwargs['pk'])
        if request.method == 'GET':
            form = OrderForm(request.GET)
            if form.is_valid():
                full_name = request.GET.get('full_name')
                phone_number = request.GET.get('phone_number')
                quantity = int(request.GET.get('quantity'))

                if products.quantity >= quantity:
                    products.quantity = products.quantity - quantity
                    order = Order.objects.create(full_name=full_name,
                                                 phone_number=phone_number,
                                                 quantity=quantity,
                                                 product=products)
                    products.save()
                    order.save()
                    messages.add_message(request, messages.SUCCESS, 'Your order has been added Successfully!.')
                else:
                    messages.add_message(request, messages.ERROR, 'Quantity is raise full\'s')
        else:
            form = OrderForm()

        context = {'form': form,
                   'products': products, }
        return render(request, 'shop/detail.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = get_object_or_404(Product, id=self.kwargs['pk'])
        context['products'] = products
        context['comments'] = Comment.objects.filter(product=products, is_negative=False)
        context['related_products'] = Product.objects.filter(category_id=products.category_id)
        return context