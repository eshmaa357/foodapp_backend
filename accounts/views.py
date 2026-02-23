from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer._validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'Error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        restaurant_name = None
        if user.is_vendor:
            try:
                restaurant_name = user.vendor_profile.restaurant_name
            except Exception:
                restaurant_name = None

        return Response({
            'access':str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'role': 'vendor' if user.is_vendor else 'customer',
            'restaurant_name': restaurant_name,
        })