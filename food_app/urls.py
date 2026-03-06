from django.urls import path
from .views import (FoodListCreateView,
VendorFoodListCreateView,VendorFoodDetailView,
CustomerMenuView,PlaceOrderView,
CustomerOrderListView,
CustomerCancelOrderView,
CustomerOrderDetailView,
VendorOrderListView,
VendorOrderUpdateView,
VendorMenuView, SubmitRatingView,VendorRatingListView,
VendorAverageRatingView)


urlpatterns = [
    path('fooditems/', FoodListCreateView.as_view(), name='food-list'),

    path('vendor/',VendorFoodListCreateView.as_view(), name='vendor-food-list-create'),
    path('vendor/<int:pk>/', VendorFoodDetailView.as_view(),name='vendor-food-detail'),

    path('menu/', CustomerMenuView.as_view(),name='customer-menu'),
    
    # Customer order endpoints
    path('orders/place/', PlaceOrderView.as_view(), name='place-order'),
    path('orders/my/', CustomerOrderListView.as_view(), name='customer-orders'),
    path('orders/<int:pk>/cancel/', CustomerCancelOrderView.as_view(), name='cancel-order'),

    path('orders/<int:pk>/',CustomerOrderDetailView.as_view(),name='customer-order-detail'),

    # Vendor order endpoints
    path('orders/vendor/', VendorOrderListView.as_view(), name='vendor-orders'),
    path('orders/vendor/<int:pk>/update/', VendorOrderUpdateView.as_view(), name='vendor-order-update'),

    path('menu/vendor/<int:vendor_id>/', VendorMenuView.as_view(), name='vendor-menu'),

    path('ratings/submit/<int:vendor_order_id>/', SubmitRatingView.as_view(), name='submit-rating'),
    path('ratings/vendor/<int:vendor_id>/', VendorRatingListView.as_view(), name='vendor-ratings'),
    path('ratings/vendor/<int:vendor_id>/average/', VendorAverageRatingView.as_view(), name='vendor-average-rating'),
]
