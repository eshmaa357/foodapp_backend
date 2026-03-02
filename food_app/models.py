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
    
class FoodItemHistory(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='history')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=[
        ('CREATED','Created'),
        ('UPDATED', 'Updated'),
        ('DELETED', 'Deleted'),
    ])

    def __str__(self):
        return f"{self.name} - {self.action} at {self.changed_at}"
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('picked', 'Picked'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"


class VendorOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('picked', 'Picked'),
        ('cancelled', 'Cancelled'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='vendor_orders')
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='vendor_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"VendorOrder #{self.id} - {self.vendor.restaurant_name} - {self.status}"
    def status_color(self):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#007bff',
            'preparing': '#fd7e14',
            'ready': '#28a745',
            'picked': '#17a2b8',
            'cancelled': '#dc3545'
        }
        return colors.get(self.status, '#dc3545')


class OrderItem(models.Model):
    vendor_order = models.ForeignKey(VendorOrder, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"

    def get_total(self):
        return self.price * self.quantity