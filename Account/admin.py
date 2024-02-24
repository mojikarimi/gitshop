# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserUserChangeForm
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserUserChangeForm
    modulefinder = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('CustomField', {'fields': ('image', 'verify_code', 'national_number', 'card_number', 'phone_number')}),
    )  # To display the fields in the superuser panel


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Permission)
