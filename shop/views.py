from django.shortcuts import render, get_object_or_404
from shop.models import Product


# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


def product_detail(request,pk):
    products = get_object_or_404(Product, id=pk)
    context = {'products': products}
    return render(request,'shop/detail.html',context)

def about(request):
    return render(request,'shop/index2.html')