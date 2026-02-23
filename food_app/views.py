from rest_framework import generics, permissions
from .serializers import FoodSerializer
from .models import FoodItem
from vendor.models import VendorProfile


class FoodListCreateView(generics.ListCreateAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodSerializer

class VendorFoodListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = VendorProfile.objects.get(user=self.request.user)
        return FoodItem.objects.filter(vendor=vendor)
    
    def perform_create(self, serializer):
        vendor = VendorProfile.objects.get(user=self.request.user)
        serializer.save(vendor=vendor)

class VendorFoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = VendorProfile.objects.get(user=self.request.user)
        return FoodItem.objects.filter(vendor=vendor)