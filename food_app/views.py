from rest_framework import generics, permissions
from .models import FoodItem
from .serializers import FoodItemSerializer
from vendor.models import VendorProfile
from django.shortcuts import get_object_or_404

# Customers - view all available food items (no auth required)
class FoodListCreateView(generics.ListAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return FoodItem.objects.filter(is_available=True)

# Vendors - list and add their own food items
class VendorFoodListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = VendorProfile.objects.get(user=self.request.user)
        return FoodItem.objects.filter(vendor=vendor)

    def perform_create(self, serializer):
        vendor = VendorProfile.objects.get(user=self.request.user)
        serializer.save(restaurant=vendor)

# Vendors - edit or delete their own food item
class VendorFoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = VendorProfile.objects.get(user=self.request.user)
        return FoodItem.objects.filter(restaurant=vendor)


