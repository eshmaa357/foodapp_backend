from rest_framework import serializers
from .models import VendorProfile

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = '__all__'
        read_only_fields = ['user']