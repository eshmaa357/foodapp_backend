from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User, CustomerProfile

class CustomUserForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.is_vendor:
                self.fields['role'].initial = 'vendor'
            else:
                self.fields['role'].initial = 'customer'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['role'] == 'vendor':
            user.is_vendor = True
            user.is_customer = False
        else:
            user.is_vendor = False
            user.is_customer = True
        if commit:
            user.save()
        return user

class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(CustomerProfile)