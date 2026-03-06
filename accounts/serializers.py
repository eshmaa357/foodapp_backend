from rest_framework import serializers
from .models import User,CustomerProfile
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','is_vendor','is_customer']
        extra_kwargs = {'password':{'write_only':True}}

        def create(self,validated_data):
            user = User.objects.create_user(**validated_data)
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class CustomerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = CustomerProfile
        fields = ['id', 'username','email','phone_number','profile_picture','address']

    def update(self,instance,validated_data):
        user_data = validated_data.pop('user',{})
        if 'email' in user_data:
            instance.user.email = user_data['email']
            instance.user.save()
        return super().update(instance,validated_data)

class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

























# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
#     password2 = serializers.CharField(write_only = True, required = True)
#     is_vendor = serializers.BooleanField(default = False)

#     class Meta:
#         model = User
#         fields = ('username','email','password','password2','is_vendor')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({'password':"Password fields didn't match"})
#         return attrs
    
#     def create(self,validated_data):
#         validated_data.pop('password2')
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             is_vendor=validated_data['is_vendor']
#         )

#         user.set_password(validated_data['password'])
#         user.save()
#         return user
