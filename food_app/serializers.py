from rest_framework import serializers
from .models import FoodItem


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'