from django.contrib import admin
from .models import Roles, User

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff')
    filter_horizontal = ('role',)  # to manage many-to-many field in the admin
    search_fields = ('username', 'email', 'first_name', 'last_name')
