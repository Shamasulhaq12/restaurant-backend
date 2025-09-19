from rest_framework import serializers

from apps.restaurants.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'order', 'user', 'rate', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'order']

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'order', 'rate', 'comment']
        read_only_fields = ['id']

    def validate_rate(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rate must be between 1 and 5.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data['user'] = request.user.profile
        return super().create(validated_data)