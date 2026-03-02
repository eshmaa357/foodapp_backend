from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import FoodItem, FoodItemHistory, Order, VendorOrder, OrderItem
from .serializers import FoodItemSerializer, OrderSerializer, VendorOrderSerializer
from vendor.models import VendorProfile
from django.shortcuts import get_object_or_404
import hashlib
from datetime import date
import random
from rest_framework.views import APIView
from collections import defaultdict
from rest_framework import status


# Customers - view all available food items (no auth required)
class FoodListCreateView(generics.ListAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return FoodItem.objects.filter(is_available=True)

# Vendors - list and add their own food items
class VendorFoodListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = VendorProfile.objects.get(user=self.request.user)
        return FoodItem.objects.filter(restaurant=vendor)

    def perform_create(self, serializer):
        vendor = VendorProfile.objects.get(user=self.request.user)
        food = serializer.save(restaurant=vendor)
        FoodItemHistory.objects.create(
            food_item = food,
            name = food.name,
            description = food.description,
            price = food.price,
            is_available = food.is_available,
            action = 'CREATED'
        )

# Vendors - edit or delete their own food item
class VendorFoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = VendorProfile.objects.get(user=self.request.user)
        return FoodItem.objects.filter(restaurant=vendor)
    
    def perform_update(self, serializer):
        food = serializer.save()
        FoodItemHistory.objects.create(
            food_item = food,
            name = food.name,
            description = food.description,
            price = food.price,
            is_available = food.is_available,
            action = 'UPDATED'
        )

    def perform_destroy(self, instance):
        FoodItemHistory.objects.create(
            food_item = instance,
            name = instance.name,
            description = instance.description,
            price = instance.price,
            is_available = instance.is_available,
            action='DELETED'
        )
        instance.delete()

class CustomerMenuView(generics.ListAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        all_items = []

        vendors = VendorProfile.objects.all()
        today = date.today().isoformat()

        for vendor in vendors:
            available_items = list(
                FoodItem.objects.filter(restaurant=vendor, is_available=True)
            )
            if not available_items:
                        continue

            if vendor.is_static_menu:
                # Static vendor - show all items
                all_items.extend(available_items)
            else:
                # Rotating vendor - show half the items, rotated daily
                half = max(1, len(available_items) // 2)

                # Use date + vendor id as seed for consistent daily rotation
                seed_str = f"{today}-{vendor.id}"
                seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)

        # Shuffle based on seed
                rng = random.Random(seed)
                shuffled = available_items.copy()
                rng.shuffle(shuffled)

                all_items.extend(shuffled[:half])

                return all_items      


# Customer - place an order
class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        items_data = request.data.get('items', [])  # [{food_item_id, quantity}]
        note = request.data.get('note', '')

        if not items_data:
            return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Group items by vendor
        vendor_items = defaultdict(list)
        for item_data in items_data:
            try:
                food_item = FoodItem.objects.get(id=item_data['food_item_id'], is_available=True)
                vendor_items[food_item.restaurant].append({
                    'food_item': food_item,
                    'quantity': item_data.get('quantity', 1)
                })
            except FoodItem.DoesNotExist:
                return Response({'error': f"Food item {item_data['food_item_id']} not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Create main order
        order = Order.objects.create(customer=request.user, note=note)
        total_price = 0

        # Create vendor sub-orders
        for vendor, items in vendor_items.items():
            vendor_order = VendorOrder.objects.create(order=order, vendor=vendor)
            subtotal = 0

            for item_data in items:
                food_item = item_data['food_item']
                quantity = item_data['quantity']
                price = food_item.price

                OrderItem.objects.create(
                    vendor_order=vendor_order,
                    food_item=food_item,
                    quantity=quantity,
                    price=price
                )
                subtotal += price * quantity

            vendor_order.subtotal = subtotal
            vendor_order.save()
            total_price += subtotal

        order.total_price = total_price
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class CustomerOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

# Customer - view their orders
class CustomerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')


# Customer - cancel their order (only if pending)
class CustomerCancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(id=pk, customer=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if any vendor order is not pending
        non_pending = order.vendor_orders.exclude(status='pending')
        if non_pending.exists():
            return Response({'error': 'Cannot cancel order after it has been confirmed'}, status=status.HTTP_400_BAD_REQUEST)

        order.vendor_orders.all().update(status='cancelled')
        return Response({'message': 'Order cancelled successfully'})


# Vendor - view their incoming orders
class VendorOrderListView(generics.ListAPIView):
    serializer_class = VendorOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = VendorProfile.objects.get(user=self.request.user)
        queryset = VendorOrder.objects.filter(vendor=vendor).order_by('-created_at')

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


# Vendor - update order status
class VendorOrderUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            vendor = VendorProfile.objects.get(user=self.request.user)
            vendor_order = VendorOrder.objects.get(id=pk, vendor=vendor)
        except (VendorProfile.DoesNotExist, VendorOrder.DoesNotExist):
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        valid_statuses = ['confirmed', 'preparing', 'ready', 'picked', 'cancelled']

        if new_status not in valid_statuses:
            return Response({'error': f'Invalid status. Choose from {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)

        if vendor_order.status == 'picked':
            return Response({'error': 'Cannot update a picked up order'}, status=status.HTTP_400_BAD_REQUEST)

        vendor_order.status = new_status
        vendor_order.save()

        return Response(VendorOrderSerializer(vendor_order).data)
    
class VendorMenuView(generics.ListAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        return FoodItem.objects.filter(restaurant__id==vendor_id,is_available=True)