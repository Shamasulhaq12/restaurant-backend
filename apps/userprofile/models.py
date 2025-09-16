from django.db import models
from apps.core.models import User
from coresite.mixin import AbstractTimeStampModel

USER_TYPE_CHOICES = (
    ('admin', 'Admin'),
    ('customer', 'Customer'),
    ('waiter', 'waiter'),
)
class UserProfile(AbstractTimeStampModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='customer')
    # employee_restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.first_name+' '+self.last_name

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
