from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "content")
    list_filter = ("published_date", "author")
    ordering = ("-published_date",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at", "updated_at")
    search_fields = ("content", "author__username", "post__title")
    list_filter = ("created_at", "author")
    ordering = ("-created_at",)