from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .models import Order
from .models import OrderLineItem
from .forms import OrderForm
from products.models import Product
from shopping_bag.contexts import shopping_bag_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'shopping_bag': json.dumps(request.session.get('shopping_bag', {})),  # noqa
            'save_info': request.POST.get('save_info'),
            'username': request.user.username if request.user.is_authenticated else None  # noqa
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'We apologize, but we are currently unable to \
                       process your payment. Please give it another try later.\
                         Thank you for your patience!')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        shopping_bag = request.session.get('shopping_bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            order.original_shopping_bag = json.dumps(shopping_bag)
            order.save()

            request.session['save_info'] = 'save-info' in request.POST

            # Stripe payment processing
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

            # Redirect to a page where the Stripe payment can be confirmed
            return redirect(reverse('stripe_confirm_payment', args=[order.order_number]))  # noqa

        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')  # noqa

    else:
        shopping_bag = request.session.get('shopping_bag', {})

    if not shopping_bag:
        messages.error(request, "Oops, your shopping bag is empty.")
        return redirect(reverse('products'))

    current_shopping_bag = shopping_bag_contents(request)
    total = current_shopping_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')  # noqa

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'shopping_bag' in request.session:
        del request.session['shopping_bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
