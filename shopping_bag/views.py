from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Create your views here.


def view_shopping_bag(request):
    """ A view to show the products on the shopping bag """
    return render(request, 'shopping_bag/shopping_bag.html')


def add_to_shopping_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')
    shopping_bag = request.session.get('shopping_bag', {})

    if item_id in list(shopping_bag.keys()):
        shopping_bag[item_id] += quantity
    else:
        shopping_bag[item_id] = quantity

    request.session['shopping_bag'] = shopping_bag
    print(request.session['shopping_bag'])
    return redirect(redirect_url)
