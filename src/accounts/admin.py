from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = (
        'username', 'email', 'email_verified', 'is_active', 'is_staff', 'is_superuser', 'created'
    )
    list_filter = ('is_active', 'is_staff', 'email_verified')
    search_fields = ('username', 'email')
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('email_verified', 'display_name', 'image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email_verified', 'display_name', 'email', 'image')}),
    )
