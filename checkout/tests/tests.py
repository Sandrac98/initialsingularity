from django.test import TestCase
from django.urls import reverse
from products.models import Product


class CheckoutTestCase(TestCase):
    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            price=10.0,
        )

    def test_checkout_empty_shopping_bag(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)

    def test_checkout_with_products(self):
        # Simulate adding a product to the shopping bag
        self.client.post(reverse('add_to_shopping_bag',
                                 args=[self.product.id]), {
            'quantity': 1,
            'redirect_url': reverse('shopping_bag'),
        })

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout.html")
        self.assertContains(response, "Test Product")
