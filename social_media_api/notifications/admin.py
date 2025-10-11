from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "actor", "verb", "timestamp", "read")
    list_filter = ("read", "timestamp")
    search_fields = ("recipient__username", "actor__username", "verb")
