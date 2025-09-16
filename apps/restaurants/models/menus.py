from django.db import models
from apps import restaurants
from coresite.mixin import AbstractTimeStampModel


class Menu(AbstractTimeStampModel):
    """
    Model representing a models item.
    """
    restaurant = models.ForeignKey("restaurants.Restaurant",
                                   related_name='menus', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class MenuItem(AbstractTimeStampModel):
    """
    Model representing a models item.
    """
    menu = models.ForeignKey("restaurants.Menu",
                             related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey(
        "restaurants.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="menu_items"
    )

    def __str__(self):
        return f"{self.name} - {self.menu.name}"

class MenuItemIngredient(AbstractTimeStampModel):
    """
    Model representing an ingredient for a models item.
    """
    menu_item = models.ForeignKey("restaurants.MenuItem",
                                  related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='ingredients/', blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.name} - {self.menu_item.name}"
