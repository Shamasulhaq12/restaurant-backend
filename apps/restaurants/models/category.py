from django.db import models

from coresite.mixin import AbstractTimeStampModel


class Category(AbstractTimeStampModel):
    """
    Simple category for grouping menu items (e.g. Pizza, Drinks, Desserts).
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
