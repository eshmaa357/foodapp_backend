from django.urls import path
from .views import FoodListCreateView,VendorFoodListCreateView,VendorFoodDetailView


urlpatterns = [
    path('fooditems/', FoodListCreateView.as_view(), name='food-list'),
    path('vendor/',VendorFoodListCreateView.as_view(), name='vendor-food-list-create'),
    path('vendor/<int:pk>/', VendorFoodDetailView.as_view(),name='vendor-food-detail')
]