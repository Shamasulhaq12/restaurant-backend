from django.db import models

from apps import userprofile, restaurants
from coresite.mixin import AbstractTimeStampModel

PAYMENT_STATUS = (
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
)

class PaymentDetails(AbstractTimeStampModel):
    user = models.ForeignKey('userprofile.UserProfile', on_delete=models.CASCADE)
    order = models.ForeignKey('restaurants.Orders', on_delete=models.CASCADE)
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True)
    payment_method = models.CharField(max_length=255, choices=[
        ("cash on delivery", "Cash on Delivery"),
        ("transfer", "Transfer"),
    ], default='cash on delivery')
    payment_status = models.CharField(max_length=255, default='Pending', choices=PAYMENT_STATUS)
    payment_date = models.DateTimeField(auto_now_add=True)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)

    class Meta:
        db_table = 'payment_details'
        verbose_name = 'Payment Detail'
        verbose_name_plural = 'Payment Details'