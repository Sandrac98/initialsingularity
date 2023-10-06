from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import Product, Category


class ProductViewsTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
        )
        self.category = Category.objects.create(
            name='Test Category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Description for test product',
            price=10.0,
            category=self.category
        )
        self.image = SimpleUploadedFile(
            "test_image.jpg", content=b'', content_type="image/jpg"
        )

    def test_all_products_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_details_view(self):
        response = self.client.get(reverse('product_details',
                                           args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_details.html')

    def test_add_product_view_authenticated(self):
        self.client.login(username='admin', password='adminpassword')
        form_data = {
            'name': 'New Test Product',
            'description': 'Description for new test product',
            'price': 15.0,
            'category': self.category.id,
            'image': self.image,
        }
        response = self.client.post(reverse('add_product'),
                                    data=form_data,
                                    format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(
            name='New Test Product').exists())

    def test_add_product_view_unauthenticated(self):
        form_data = {
            'name': 'New Test Product',
            'description': 'Description for new test product',
            'price': 15.0,
            'category': self.category.id,
            'image': self.image,
        }
        response = self.client.post(reverse('add_product'),
                                    data=form_data, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(
            name='New Test Product').exists())

    def test_edit_product_view_authenticated(self):
        self.client.login(username='admin', password='adminpassword')
        form_data = {
            'name': 'Edited Test Product',
            'description': 'Updated description',
            'price': 20.0,
            'category': self.category.id,
        }
        response = self.client.post(reverse('edit_product',
                                            args=[self.product.id]),
                                    data=form_data)
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Edited Test Product')

    def test_add_product_view_unauthenticated(self):
        form_data = {
            'name': 'New Test Product',
            'description': 'Description for new test product',
            'price': 15.0,
            'category': self.category.id,
            'image': self.image,
        }
        response = self.client.post(reverse('add_product'),
                                    data=form_data, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(
            name='New Test Product').exists())

    def test_delete_product_view_authenticated(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('delete_product',
                                            args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(name='Test Product').exists())

    def test_delete_product_view_unauthenticated(self):
        response = self.client.post(reverse('delete_product',
                                            args=[self.product.id]))
        self.assertTrue(Product.objects.filter(name='Test Product').exists())