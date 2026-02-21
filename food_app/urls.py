from django.urls import path
from .views import FoodListCreateView

urlpatterns = [
    path('fooditems/', FoodListCreateView.as_view(), name='food-list'),
]