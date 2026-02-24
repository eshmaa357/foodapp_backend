from django.db import models
from django.conf import settings
from vendor.models import VendorProfile

# Create your models here.
class FoodItem(models.Model):
    restaurant = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='foods', null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='food_images/', blank=True,null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        restaurant_name = self.restaurant.restaurant_name if self.restaurant else "No Vendor"
        return f"{self.name} ({restaurant_name})"