from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """A profile model designed to manage default shipping details
      and track order history."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    defaul_phone_number = models.CharField(max_length=20, null=True, blank=True)  # noqa
    defaul_street_address1 = models.CharField(max_length=80, null=True, blank=True)  # noqa
    defaul_street_address1 = models.CharField(max_length=80, null=True, blank=True)  # noqa
    defaul_town_or_city = models.CharField(max_length=40, null=True, blank=True)  # noqa
    defaul_postcode = models.CharField(max_length=20, null=True, blank=True)
    defaul_country = CountryField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """ Create or update the user profile"""
    if created:
        UserProfile.objects.create(user=instance)
        # Existing users: just save the profile
        instance.userprofile.save()
