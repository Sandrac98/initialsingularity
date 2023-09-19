from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def all_products(request):
    """ Show all products """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """ Shows products details """

    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_details.html', context)
