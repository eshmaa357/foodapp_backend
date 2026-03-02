from django.contrib import admin
from .models import FoodItem,FoodItemHistory, Order, VendorOrder, OrderItem

# Register your models here.
admin.site.register(FoodItem)
admin.site.register(FoodItemHistory)
admin.site.register(Order)
admin.site.register(VendorOrder)
admin.site.register(OrderItem)
