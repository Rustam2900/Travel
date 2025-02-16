from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role

admin.site.register(Role)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'age', 'role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'age', 'profile_image', 'role')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
