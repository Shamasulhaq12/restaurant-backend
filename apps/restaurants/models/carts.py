from django.db import models
from apps import userprofile, restaurants
from coresite.mixin import AbstractTimeStampModel


class Cart(AbstractTimeStampModel):
    """
    Model representing a shopping cart.
    """
    user = models.ForeignKey('userprofile.UserProfile',
                             on_delete=models.CASCADE, related_name='user_carts')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart for {self.user.first_name} {self.user.last_name}"


class CartItem(AbstractTimeStampModel):
    """
    Model representing an item in the shopping cart.
    """
    cart = models.ForeignKey("restaurants.Cart", on_delete=models.CASCADE, related_name='cart_items')
    menu_item = models.ForeignKey('restaurants.MenuItem', on_delete=models.CASCADE, related_name='menu_item_cart_items')
    quantity = models.PositiveIntegerField(default=1)
    comments = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in {self.cart}"
