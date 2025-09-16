from rest_framework import serializers
from apps.restaurants.models import Orders, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = "__all__"