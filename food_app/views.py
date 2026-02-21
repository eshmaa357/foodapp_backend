from rest_framework import generics
from .models import FoodItem
from .serializers import FoodSerializer


class FoodListCreateView(generics.ListCreateAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodSerializer