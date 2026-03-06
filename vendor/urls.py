from django.urls import path
from .views import (
    VendorProfileView,
    VendorLoginView,
    VendorLogoutView,
    VendorDashboardView,
    VendorProfilePageView,
    VendorFoodPageView,
    VendorFoodAddView,
    VendorFoodEditView,
    VendorFoodDeleteView,
    VendorFoodHistoryView,
    VendorFoodDetailPageView,
    VendorOrderPageView,
    VendorOrderUpdatePageView, VendorRatingPageView
)

urlpatterns = [
    path('profile/', VendorProfileView.as_view(), name='vendor-profile'),

    path('login/', VendorLoginView.as_view(), name='vendor-login'),
    path('logout', VendorLogoutView.as_view(), name='vendor-logout'),

    path('dashboard/', VendorDashboardView.as_view(), name='vendor-dashboard'),

    path('profile-page/', VendorProfilePageView.as_view(), name='vendor-profile-page'),
    
    path('foods/', VendorFoodPageView.as_view(), name='vendor-food-page'),
    path('foods/add/', VendorFoodAddView.as_view(), name='vendor-food-add'),
    path('foods/edit/<int:pk>/', VendorFoodEditView.as_view(), name='vendor-food-edit'),
    path('foods/delete/<int:pk>/', VendorFoodDeleteView.as_view(), name='vendor-food-delete'),
    path('foods/history/', VendorFoodHistoryView.as_view(), name='vendor-food-history'),
    path('foods/<int:pk>/', VendorFoodDetailPageView.as_view(), name='vendor-food-detail-page'),

    path('orders/', VendorOrderPageView.as_view(), name='vendor-order-page'),
    path('orders/<int:pk>/update/', VendorOrderUpdatePageView.as_view(), name='vendor-order-update-page'),

    path('ratings/',VendorRatingPageView.as_view(),name='vendor-rating-page'),
]

