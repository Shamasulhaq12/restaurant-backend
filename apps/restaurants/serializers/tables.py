from rest_framework import serializers
from apps.restaurants.models import Table


class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    waiter_name = serializers.CharField(source="waiter.user.username", read_only=True)  # assuming UserProfile → User relation

    class Meta:
        model = Table
        fields = [
            "id",
            "restaurant",
            "restaurant_name",
            "table_number",
            "waiter",
            "waiter_name",
            "qr_code",
            "created_at",
            "updated_at",
        ]
