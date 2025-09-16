from rest_framework import serializers
from apps.restaurants.models import Menu, MenuItem, MenuItemIngredient, RestaurantImage, Restaurant


class RestaurantImageSerializer(serializers.ModelSerializer):
    """
    Serializer for RestaurantImage model.
    """
    class Meta:
        model = RestaurantImage
        fields = ['id', 'restaurant', 'image', 'is_primary']
        read_only_fields = ['id', 'restaurant']

class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant model.
    """
    images = RestaurantImageSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'address', 'phone_number', 'email', 'images']
        read_only_fields = ['id']

class MenuItemIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for MenuItemIngredient model.
    """
    class Meta:
        model = MenuItemIngredient
        fields = ['id', 'menu_item', 'name', 'image', 'quantity', 'description']
        read_only_fields = ['id', 'menu_item']

class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for MenuItem model.
    """
    ingredients = MenuItemIngredientSerializer(many=True, read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'menu', 'name', 'image', 'description', 'price', 'ingredients']
        read_only_fields = ['id', 'menu']

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for Menu model.
    """
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'name', 'description', 'menu_items']
        read_only_fields = ['id', 'restaurant']