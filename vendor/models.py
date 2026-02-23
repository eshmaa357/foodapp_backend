from django.db import models
from django.conf import settings

# Create your models here.
class VendorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_profile')
    restaurant_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True,null=True)
    logo = models.ImageField(upload_to='vendor_logos/',blank=True,null=True)
    
    def __str__(self):
        return self.restaurant_name
    

