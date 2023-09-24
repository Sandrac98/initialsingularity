from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    shopping_bag = request.session.get('shopping_bag', {})
    if not shopping_bag:
        messages.error(request, "Oops your shopping bag is empty")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_live_51NkAq5BiTgslsQtRJoHaGDaFj6dCKRDLeeq3FJ5kY70nkxjxTHUKpuuZa7Y2sPXxb4kdzSXi7cR4WIbRPvQhA8MP00yaR1bh8T',  # noqa
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
