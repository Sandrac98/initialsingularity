from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product
from .models import UserProfile

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ Handle payment_intent_succeeded webhook from Stripe"""
        intent = event.data.object
        pid = intent.id
        shopping_bag = intent.metadata.shopping_bag
        save_info = intent.metadata.save_info

        billing_details = intent.chanrges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
            profile = None
            username = intent.metadata.username
            if username != 'AnonymousUser':
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_phone_number = shipping_details.phone
                    profile.default_street_address1 = shipping_details.address.line1  # noqa
                    profile.default_street_address2 = shipping_details.address.line2  # noqa
                    profile.default_postcode = shipping_details.address.postal_code  # noqa
                    profile.default_town_or_city = shipping_details.address.city  # noqa
                    profile.default_country = shipping_details.address.country
                    profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=shipping_details.email,
                    phone_number__iexact=shipping_details.phone,
                    street_address1__iexact=shipping_details.line1,
                    street_address2__iexact=shipping_details.line2,
                    town_or_city__iexact=shipping_details.city,
                    postcode__iexact=shipping_details.postal_code,
                    country__iexact=shipping_details.country,
                    grand_total=grand_total,
                    original_shopping_bag=shopping_bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
            if order_exists:
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',  # noqa
                    status=200)
            else:
                order: None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        user_profile=profile,
                        email=shipping_details.email,
                        phone_number=shipping_details.phone,
                        street_address1=shipping_details.line1,
                        street_address2=shipping_details.line2,
                        town_or_city=shipping_details.city,
                        postcode=shipping_details.postal_code,
                        country=shipping_details.country,
                        grand_total=grand_total,
                        original_shopping_bag=shopping_bag,
                        stripe_pid=pid,
                    )
                    for item_id, item_data in json.loads(shopping_bag).items():
                        product = Product.objects.get(id=item_id)
                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                                )
                            order_line_item.save(
                                )
                except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(
                        content=f'Webhook recieved: {event["type"]} | ERROR {e}',  # noqa
                    )
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ Handle payment_inten.payment_failed webhook from Stripe"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
