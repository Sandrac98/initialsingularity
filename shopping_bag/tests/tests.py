from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product


class ShoppingBagTestCase(TestCase):

    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            price=10.0,
        )

    def test_shopping_bag(self):
        response = self.client.get(reverse('shopping_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_bag/shopping_bag.html')

    def test_shopping_bag_is_empty(self):
        response = self.client.get(reverse('shopping_bag'))
        self.assertEqual(len(response.context['shopping_bag_items']), 0)

    def test_add_to_shopping_bag(self):
        # Simulate a POST request to add a product to the shopping bag
        response = self.client.post(reverse('add_to_shopping_bag',
                                            args=[self.product.id]), {
            'quantity': 2,
            'redirect_url': reverse('shopping_bag'),
        })
        response = self.client.get(reverse('shopping_bag'))
        self.assertContains(response, 'Test Product')
        self.assertEqual(len(response.context['shopping_bag_items']), 1)

    def test_update_shopping_bag(self):
        self.client.post(reverse('add_to_shopping_bag',
                                 args=[self.product.id]), {
            'quantity': 1,
            'redirect_url': reverse('shopping_bag'),
        })

        # Simulate a POST request to update the quantity of
        # the product in the shopping bag
        response = self.client.post(reverse('update_shopping_bag',
                                            args=[self.product.id]), {
            'quantity': 3,
            'redirect_url': reverse('shopping_bag'),
        })

        response = self.client.get(reverse('shopping_bag'))
        self.assertContains(response, 'Test Product')
        self.assertEqual(len(response.context['shopping_bag_items']), 1)

    def test_remove_from_shopping_bag(self):
        self.client.post(reverse('add_to_shopping_bag',
                                 args=[self.product.id]), {
            'quantity': 1,
            'redirect_url': reverse('shopping_bag'),
        })

        # Simulate a POST request to remove the product from the shopping bag
        response = self.client.post(reverse('remove_from_shopping_bag',
                                            args=[self.product.id]))

        shopping_bag = self.client.session.get('shopping_bag', {})
        self.assertFalse(self.product.id in shopping_bag)
