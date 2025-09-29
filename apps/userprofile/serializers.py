from django.db import transaction, IntegrityError
from rest_framework import serializers
from .models import UserProfile, User
from ..restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'address', 'phone_number', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    user_type = serializers.CharField(source='user.user_type', read_only=True)
    restaurants = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_restaurants(self, obj):
        user = obj.user
        if user.user_type == 'restaurant_owner':
            return RestaurantSerializer(user.owned_restaurants.all(), many=True).data
        elif user.user_type == 'waiter' and hasattr(user, 'waiter'):
            return RestaurantSerializer(user.waiter.restaurant).data
        return []

class UserProfileWriteSerializer(serializers.ModelSerializer):
    # Include user fields for creation/update
    email = serializers.EmailField(source="user.email")
    username = serializers.CharField(source="user.username")
    password = serializers.CharField(source="user.password", write_only=True, required=False)
    user_type = serializers.ChoiceField(source="user.user_type", choices=User._meta.get_field("user_type").choices)
    restaurants = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id", "first_name", "last_name", "phone", "bio", "image",
            "email", "username", "password", "user_type", 'restaurants',
        ]

    def get_restaurants(self, obj):
        user = obj.user
        if user.user_type == 'restaurant_owner':
            return RestaurantSerializer(user.owned_restaurants.all(), many=True).data
        elif user.user_type == 'waiter' and hasattr(user, 'waiter'):
            return RestaurantSerializer(user.waiter.restaurant).data
        return []

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = user_data.pop("password", None)

        # Create user
        try:
            with transaction.atomic():
                user = User.objects.create(**user_data)
                if password:
                    user.set_password(password)
                    user.save()

                user.is_active = True
                if user in ['waiter', 'restaurant_owner'] :
                    user.is_staff = True

                user.save()
                # Create profile
                profile = UserProfile.objects.create(user=user, **validated_data)
                return profile

        except IntegrityError as e:
            if 'core_user.email' in str(e):
                raise serializers.ValidationError({"email": "A user with that email already exists."})
            elif 'core_user.username' in str(e):
                raise serializers.ValidationError({"username": "A user with that username already exists."})
            raise serializers.ValidationError({"error": str(e)})



    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        password = user_data.pop("password", None)

        # Update User fields
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        if password:
            instance.user.set_password(password)
        instance.user.save()

        # Update Profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
