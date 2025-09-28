from django.contrib import admin
from .models import Book

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns shown in the list view
    list_display = ("title", "author", "publication_year")

    # Right-side filters
    list_filter = ("publication_year", "author")

    # Top search box (case-insensitive icontains)
    search_fields = ("title", "author")

    # Optional niceties
    ordering = ("title",)                 # default sort
    list_per_page = 25 