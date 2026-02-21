from django.shortcuts import render
from .models import VendorProfile
from .serializers import VenforProfileSerializer
from rest_framework import generics,permissions

# Create your views here.
class VendorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = VenforProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_object(self):
    # Only allow the logged-in vendor to access their profile
        return self.request.user.vendor_profile