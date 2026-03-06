from rest_framework import serializers
from .models import FoodItem, Order, VendorOrder, OrderItem,Rating

class FoodItemSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.restaurant_name', read_only=True)

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'price', 'image', 'is_available', 'created_at', 'restaurant_name']
        read_only_fields = ['restaurant', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.CharField(source='food_item.name', read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'food_item', 'food_item_name', 'quantity', 'price', 'total']

    def get_total(self, obj):
        return obj.get_total()


class VendorOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    vendor_name = serializers.CharField(source='vendor.restaurant_name', read_only=True)
    customer_name = serializers.CharField(source='order.customer.username', read_only=True)
    customer_email = serializers.SerializerMethodField()


    class Meta:
        model = VendorOrder
        fields = ['id', 'vendor','customer_name','customer_email', 'vendor_name', 'status', 'subtotal', 'items', 'created_at']

    def get_customer_email(self,obj):
        try:
            return obj.order.customer.email
        except:
            return None


class OrderSerializer(serializers.ModelSerializer):
    vendor_orders = VendorOrderSerializer(many=True, read_only=True)
    customer_username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_username', 'total_price', 'note', 'vendor_orders', 'created_at']
        read_only_fields = ['customer', 'total_price']

class RatingSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.username',read_only=True)
    vendor_name = serializers.CharField(source='vendor.restaurant_name',read_only=True)

    class Meta:
        model = Rating
        fields = ['id','customer_username','vendor_name','order','stars','created_at']
        read_only_fields = ['customer','vendor','created_at']

    def validate_stars(seld,value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Stars must be betweem 1 and 5')
        return value