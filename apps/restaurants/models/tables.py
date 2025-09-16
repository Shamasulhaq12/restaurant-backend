import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from .restaurants import Restaurant
from  apps import userprofile

from coresite.mixin import AbstractTimeStampModel


class Table(AbstractTimeStampModel):
    """
    A physical table inside a restaurant with an assigned waiter and QR code.
    """
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="tables"
    )
    table_number = models.PositiveIntegerField()
    waiter = models.ForeignKey(
        "userprofile.UserProfile",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="assigned_tables"
    )
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    class Meta:
        unique_together = ("restaurant", "table_number")  # Each table number must be unique per restaurant

    def __str__(self):
        return f"Table {self.table_number} - {self.restaurant.name}"

    def save(self, *args, **kwargs):
        """
        Auto-generate a QR code PNG for this table if not already set.
        """
        if not self.qr_code:
            qr_data = f"restaurant={self.restaurant.id}&table={self.table_number}"
            if self.waiter:
                qr_data += f"&waiter={self.waiter.id}"

            qr = qrcode.make(qr_data)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            filename = f"table_{self.restaurant.id}_{self.table_number}.png"
            self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)
