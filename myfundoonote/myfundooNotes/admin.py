from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class UserDetailsAdmin(UserAdmin):
    model = User
    ordering = ('email', 'first_name', 'last_name', 'user_name')
    list_display = ['user_name', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_name', 'password', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, UserDetailsAdmin)