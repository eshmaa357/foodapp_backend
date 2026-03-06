from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from food_app.models import FoodItemHistory
from .serializers import VendorProfileSerializer
from rest_framework import generics, permissions
import requests
from vendor.models import VendorProfile
from django.contrib.auth import get_user_model


def is_token_valid(request):
    token = request.session.get('vendor_token')
    if not token:
        return False
    
    response = requests.get(
        request.build_absolute_uri('/vendors/profile/'),
        headers={'Authorization': f'Bearer {token}'}
    )

    if response.status_code == 401:
        request.session.flush()
        return False
    
    return True

class VendorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.vendor_profile


class VendorLoginView(View):
    def get(self, request):
        if request.session.get('vendor_token'):
            return redirect('vendor-dashboard')
        return render(request, 'vendor/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        response = requests.post(
            request.build_absolute_uri('/api/accounts/login/'),
            json={'username': username, 'password': password}
        )
        if response.status_code == 200:
            data = response.json()

            if data.get('role') != 'vendor':
                return render(request, 'vendor/login.html', {'error': 'Access denied. Vendor accounts only'})

            request.session['vendor_token'] = data['access']
            request.session['username'] = data['username']
            request.session['restaurant_name'] = data.get('restaurant_name', '')
            request.session['vendor_id'] = True

            return redirect('vendor-dashboard')
        else:
            return render(request, 'vendor/login.html', {'error': 'Invalid username or password.'})


class VendorLogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('vendor-login')


class VendorDashboardView(View):
    def get(self, request):
        if not is_token_valid(request):
            return redirect('vendor-login')
        
        token = request.session['vendor_token']

        response = requests.get(
            request.build_absolute_uri('/foods/vendor/'),
            headers={'Authorization': f'Bearer {token}'}
        )
        foods = response.json() if response.status_code == 200 else []
        order_response = requests.get(
        request.build_absolute_uri('/foods/orders/vendor/'),
        headers={'Authorization': f'Bearer {token}'}
    )
        orders = order_response.json() if order_response.status_code == 200 else []

        return render(request, 'vendor/dashboard.html', {
            'food_count': len(foods),
            'order_count': len(orders),
        })


class VendorProfilePageView(View):
    def get(self, request):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        response = requests.get(
            request.build_absolute_uri('/vendors/profile/'),
            headers={'Authorization': f'Bearer {token}'}
        )

        profile = response.json() if response.status_code == 200 else {}
        return render(request, 'vendor/profile.html', {'profile': profile})

    def post(self, request):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        data = {
            'restaurant_name': request.POST.get('restaurant_name'),
            'address': request.POST.get('address'),
            'contact_number': request.POST.get('contact_number'),
        }

        files = {}
        if request.FILES.get('logo'):
            logo = request.FILES['logo']
            files = {'logo': (logo.name, logo.read(), logo.content_type)}

        response = requests.patch(
            request.build_absolute_uri('/vendors/profile/'),
            data=data,
            files=files if files else None,
            headers={'Authorization': f'Bearer {token}'}
        )

        if response.status_code == 200:
            request.session['restaurant_name'] = data['restaurant_name']
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Failed to update profile.')

        return redirect('vendor-profile-page')


class VendorFoodPageView(View):
    def get(self, request):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        response = requests.get(
            request.build_absolute_uri('/foods/vendor/'),
            headers={'Authorization': f'Bearer {token}'}
        )
        foods = response.json() if response.status_code == 200 else []
        return render(request, 'vendor/food_list.html', {'foods': foods})


class VendorFoodAddView(View):
    def get(self, request):
        if not is_token_valid(request):
            return redirect('vendor-login')
        return render(request, 'vendor/food_form.html', {'action': 'Add'})

    def post(self, request):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description'),
            'price': request.POST.get('price'),
            'is_available': request.POST.get('is_available') == 'on',
        }

        files = {}
        if request.FILES.get('image'):
            image = request.FILES['image']
            files = {'image': (image.name, image.read(), image.content_type)}

        response = requests.post(
            request.build_absolute_uri('/foods/vendor/'),
            data=data,
            files=files if files else None,
            headers={'Authorization': f'Bearer {token}'}
        )

        if response.status_code == 201:
            messages.success(request, 'Food item added successfully!')
            return redirect('vendor-food-page')
        else:
            messages.error(request, 'Failed to add food item.')
            return render(request, 'vendor/food_form.html', {'action': 'Add'})


class VendorFoodEditView(View):
    def get(self, request, pk):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        response = requests.get(
            request.build_absolute_uri(f'/foods/vendor/{pk}/'),
            headers={'Authorization': f'Bearer {token}'}
        )

        food = response.json() if response.status_code == 200 else {}
        return render(request, 'vendor/food_form.html', {'action': 'Edit', 'food': food})

    def post(self, request, pk):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description'),
            'price': request.POST.get('price'),
            'is_available': 'true' if request.POST.get('is_available') == 'on' else 'false',
        }

        files = {}
        if request.FILES.get('image'):
            image = request.FILES['image']
            files = {'image': (image.name, image.read(), image.content_type)}
        print('FILES:', request.FILES)
        print("files dict:", files)

        response = requests.patch(
            request.build_absolute_uri(f'/foods/vendor/{pk}/'),
            data=data,
            files=files if files else None,
            headers={'Authorization': f'Bearer {token}'}
        )
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code == 200:
            messages.success(request, 'Food item updated successfully!')
            return redirect('vendor-food-page')
        else:
            messages.error(request, 'Failed to update food item.')
            return redirect('vendor-food-page')


class VendorFoodDeleteView(View):
    def post(self, request, pk):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        requests.delete(
            request.build_absolute_uri(f'/foods/vendor/{pk}/'),
            headers={'Authorization': f'Bearer {token}'}
        )
        messages.success(request, 'Food item deleted.')
        return redirect('vendor-food-page')


class VendorFoodHistoryView(View):
    def get(self, request):
        if not is_token_valid(request):
            return redirect('vendor-login')

        User = get_user_model()
        user = User.objects.get(username=request.session['username'])
        vendor = VendorProfile.objects.get(user=user)
        food_ids = vendor.foods.values_list('id', flat=True)
        history = FoodItemHistory.objects.filter(food_item_id__in=food_ids).order_by('-changed_at')

        return render(request, 'vendor/food_history.html', {'history': history})

class VendorFoodDetailPageView(View):
    def get(self, request,pk):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        response = requests.get(
            request.build_absolute_uri(f'/foods/vendor/{pk}/'),
            headers={'Authorization': f'Bearer {token}'}
        )

        food = response.json() if response.status_code == 200 else {}
        return render(request, 'vendor/food_detail.html', {'food': food})
    
class VendorOrderPageView(View):
    def get(self, request):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        status_filter = request.GET.get('status','')

    
        url = request.build_absolute_uri('/foods/orders/vendor/')
        if status_filter:
            url += f'?status={status_filter}'

        response = requests.get(url, headers={'Authorization':f'Bearer {token}'})
        orders = response.json() if response.status_code == 200 else []
    
        return render(request, 'vendor/orders.html', {'orders': orders,
        'current_status': status_filter
        })


class VendorOrderUpdatePageView(View):
    def post(self, request, pk):
        if not is_token_valid(request):
            return redirect('vendor-login')

        token = request.session['vendor_token']
        new_status = request.POST.get('status')

        requests.post(
            request.build_absolute_uri(f'/foods/orders/vendor/{pk}/update/'),
            json={'status': new_status},
            headers={'Authorization': f'Bearer {token}'}
        )

        messages.success(request, f'Order status updated to {new_status}!')
        return redirect('vendor-order-page')
    
