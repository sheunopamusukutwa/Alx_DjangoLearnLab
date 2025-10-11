from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Profile', {'fields': ('bio', 'profile_picture', 'followers')}),
    )
    filter_horizontal = ('followers',)