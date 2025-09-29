from django.db import models

from apps import restaurants, core
from coresite.mixin import AbstractTimeStampModel


class Restaurant(AbstractTimeStampModel):
    """
    Model representing a restaurant.
    """
    owners = models.ManyToManyField(
        'core.User',
        related_name='owned_restaurants',
        limit_choices_to={'user_type': 'restaurant_owner'},
        blank=True
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class RestaurantImage(AbstractTimeStampModel):
    """
    Model representing an image of a restaurant.
    """
    restaurant = models.ForeignKey("restaurants.Restaurant",
                                   related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.restaurant.name}"

class Waiter(AbstractTimeStampModel):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='waiter')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='waiters')
