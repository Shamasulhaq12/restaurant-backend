from rest_framework import serializers

from apps.restaurants.models import Menu, MenuItem, MenuItemIngredient, RestaurantImage, Restaurant
from apps.userprofile.models import UserProfile


class UserProfileUserNameSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model with only username field.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username']
        read_only_fields = ['id', 'username']

class RestaurantImageSerializer(serializers.ModelSerializer):
    """
    Serializer for RestaurantImage model.
    """
    class Meta:
        model = RestaurantImage
        fields = ['id', 'restaurant', 'image', 'is_primary']
        read_only_fields = ['id', 'restaurant']

class RestaurantSerializer(serializers.ModelSerializer):
    images = RestaurantImageSerializer(many=True, read_only=True)
    image = serializers.ImageField(write_only=True, required=False)  # 👈 new
    owners = UserProfileUserNameSerializer(many=True, read_only=True)
    waiters = UserProfileUserNameSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'description',
            'address',
            'phone_number',
            'email',
            'images',
            'image',
            'owners',
            'waiters',
        ]
        read_only_fields = ['id', 'images']

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        restaurant = super().create(validated_data)
        if image:
            RestaurantImage.objects.create(
                restaurant=restaurant,
                image=image,
                is_primary=True
            )
        return restaurant

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        restaurant = super().update(instance, validated_data)
        if image:
            # replace primary image
            RestaurantImage.objects.filter(
                restaurant=restaurant,
                is_primary=True
            ).delete()
            RestaurantImage.objects.create(
                restaurant=restaurant,
                image=image,
                is_primary=True
            )
        return restaurant

class RestaurantLiteSerializer(serializers.ModelSerializer):
    """
    Lite serializer for Restaurant model.
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'name']
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