from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, Library, Librarian


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "role", "is_staff", "is_active"]
    list_filter = ["role", "is_staff", "is_active"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo", "role")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo", "role")}),
    )
    search_fields = ["username", "email"]
    ordering = ["username"]


# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)