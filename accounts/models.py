from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_vendor:
            self.is_customer = False
        super().save(*args, **kwargs)

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture=models.ImageField(upload_to='customer_profiles/')
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"