from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from checkout.models import Order
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from django.db import models


class UserProfileTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(username='testuser',
                                        password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_profile_view_redirects(self):
        response = self.client.get(reverse('profile'))
        # Check if the view redirects when not logged in
        self.assertEqual(response.status_code, 302)

    def test_create_user_creates_profile(self):
        # Create a new user with a unique username
        user = User.objects.create(username='testuser2',
                                   password='testpassword')

        # Retrieve the user's profile
        profile = UserProfile.objects.get(user=user)

        # Check if the profile is created and associated with the user
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, user)

    def test_update_user_updates_profile(self):
        # Create a user with a unique username
        user = User.objects.create(username='testuser3',
                                   password='testpassword')

        # Change some user properties
        user.username = 'updateduser'
        user.save()

        # Retrieve the user's updated profile
        profile = UserProfile.objects.get(user=user)

        # Check if the profile is updated to match the user's changes
        self.assertEqual(profile.user.username, 'updateduser')

    def test_foreignkey_cascade_delete(self):
        user_field = UserProfile._meta.get_field('user')
        self.assertEquals(
            user_field.remote_field.on_delete, models.CASCADE,
            '{} failed, value was {}'.format(user_field.name,
                                             user_field.remote_field.on_delete)
        )

    def test_order_history_view(self):
        # Create a test order
        order = Order.objects.create(order_number='123456')
        # Associate the order with the user
        order.user = self.user
        order.save()

        response = self.client.get(reverse('order_history',
                                           args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

    def test_placeholders_are_set(self):
        form = UserProfileForm()
        # Check if placeholders are set as expected for each field
        self.assertEqual(form.fields['default_phone_number']
                         .widget.attrs['placeholder'], 'Phone Number')
        self.assertEqual(form.fields['default_street_address1']
                         .widget.attrs['placeholder'], 'Street Address 1')
        self.assertEqual(form.fields['default_street_address2']
                         .widget.attrs['placeholder'], 'Street Address 2')
        self.assertEqual(form.fields['default_town_or_city']
                         .widget.attrs['placeholder'], 'Town or City')
        self.assertEqual(form.fields['default_postcode']
                         .widget.attrs['placeholder'], 'Postal Code')
