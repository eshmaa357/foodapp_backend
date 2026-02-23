from django.contrib import admin
from .models import VendorProfile
from django.contrib.auth import get_user_model

# Register your models here.
User = get_user_model()

class VendorProfileAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_vendor=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(VendorProfile,VendorProfileAdmin)
