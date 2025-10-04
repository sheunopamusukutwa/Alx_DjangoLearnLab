from django.contrib import admin
from .models import Post, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "content", "author__username", "tags__name")
    list_filter = ("published_date", "author", "tags")
    ordering = ("-published_date",)
    filter_horizontal = ("tags",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at", "updated_at")
    search_fields = ("content", "author__username", "post__title")
    list_filter = ("created_at", "author")
    ordering = ("-created_at",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
