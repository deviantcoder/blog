from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from .models import Post, Comment, Upvote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created')

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}
    

@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('author', 'body', 'created')

    def body(self, obj):
        return obj.body[:50]


@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('profile', 'post', 'created')

    def post(self, obj):
        return obj.post.title[:50]
