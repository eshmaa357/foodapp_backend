from django.urls import path
from .views import RegisterView, LoginView,CustomerProfileView,DeleteAccountView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('delete-account/',DeleteAccountView.as_view(), name='delete-account'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]