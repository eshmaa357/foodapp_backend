from rest_framework import serializers
from .models import FoodItem

class FoodItemSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.restaurant_name', read_only=True)

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'price', 'image', 'is_available', 'created_at', 'vendor_name']
        read_only_fields = ['vendor', 'created_at']