from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'display_name', 'created')

    def username(self, obj):
        return obj.user.username
