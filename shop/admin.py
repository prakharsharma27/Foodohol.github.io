from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Contact, User, Orders
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("email", "dob", 'first_name', 'last_name', "is_staff", "is_active")
    list_filter = ("email", "dob", 'last_name', "is_staff", "is_active")
    fieldsets = (
        (None, {'fields': ('email', 'dob', 'first_name', 'last_name', 'password')}),
        ("Permissions", {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'dob', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Product)
# admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(Orders)
