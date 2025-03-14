from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created')

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}
