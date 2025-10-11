from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(ListAPIView):
    """
    GET /api/notifications/
    Lists notifications for the current user: unread first, newest first.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by("read", "-timestamp")


class MarkAllReadView(APIView):
    """
    POST /api/notifications/mark-all-read/
    Marks all current user's notifications as read.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        qs = Notification.objects.filter(recipient=request.user, read=False)
        updated = qs.update(read=True)
        return Response({"updated": updated})
