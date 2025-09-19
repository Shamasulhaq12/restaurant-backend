from apps import userprofile, restaurants
from coresite.mixin import AbstractTimeStampModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(AbstractTimeStampModel):
    order = models.ForeignKey(
        'restaurants.Orders',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        'userprofile.UserProfile',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review {self.id}: {self.rate} stars"

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
