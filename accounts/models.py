from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_vendor:
            self.is_customer = False
        super().save(*args, **kwargs)