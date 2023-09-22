from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import HttpResponse

from products.models import Product
from django.contrib import messages


# Create your views here.


def view_shopping_bag(request):
    """ A view to show the products on the shopping bag """
    return render(request, 'shopping_bag/shopping_bag.html')


def add_to_shopping_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')
    shopping_bag = request.session.get('shopping_bag', {})

    if item_id in list(shopping_bag.keys()):
        shopping_bag[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {shopping_bag[item_id]}')  # noqa
    else:
        shopping_bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your shopping bag')

    request.session['shopping_bag'] = shopping_bag
    return redirect(redirect_url)


def update_shopping_bag(request, item_id):
    """ Adjust the quantity of the specified product on the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    shopping_bag = request.session.get('shopping_bag', {})

    if quantity > 0:
        shopping_bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {shopping_bag[item_id]}', extra_tags="success-toast")   # noqa

    else:
        shopping_bag.pop(item_id, None)

    request.session['shopping_bag'] = shopping_bag
    return redirect(reverse('view_shopping_bag'))


def remove_from_shopping_bag(request, item_id):
    """ Remove the specified product from the shopping bag """
    try:
        product = get_object_or_404(Product, pk=item_id)
        shopping_bag = request.session.get('shopping_bag', {})

        if item_id in shopping_bag:
            shopping_bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        else:
            pass

        request.session['shopping_bag'] = shopping_bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
