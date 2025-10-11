from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Notification

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)
    target_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "actor_username",
            "verb",
            "target_type",
            "target_object_id",
            "timestamp",
            "read",
        ]

    def get_target_type(self, obj):
        return obj.target_content_type.model if obj.target_content_type else None
