from typing import Optional
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from shop.models import Product, Category, Order
from shop.forms import OrderForm


# Create your views here.

def index(request, category_id: Optional[int] = None):
    categorys = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    context = {'products': products,
               'categorys': categorys,
    }
    return render(request, 'shop/index.html', context)


def product_detail(request,pk):
    products = get_object_or_404(Product, id=pk)
    context = {'products': products}
    return render(request,'shop/detail.html',context)

def order_detail(request,pk):
    products = get_object_or_404(Product, id=pk)
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
                messages.add_message(request, messages.SUCCESS,'Your order has been added Successfully!.')
            else:
                messages.add_message(request, messages.ERROR,'Quantity is raise full\'s')
    else:
        form = OrderForm()

    context = {'form': form,
                   'products': products,}
    return render(request, 'shop/detail.html', context)

def about(request):
    return render(request,'shop/index2.html')