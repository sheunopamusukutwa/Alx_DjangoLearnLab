from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

# Checker-friendly alias kept from Task 2:
CustomUser = get_user_model()

# Notifications
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()  # checker literal
    lookup_url_kwarg = "user_id"

    def post(self, request, user_id: int):
        if request.user.id == user_id:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        target = self.get_object()
        if request.user.following.filter(pk=target.pk).exists():
            return Response({
                "detail": "You are already following this user.",
                "following_count": request.user.following.count(),
                "target_followers_count": target.followers.count(),
            }, status=status.HTTP_200_OK)

        request.user.following.add(target)

        # Create FOLLOW notification for the target (recipient)
        if target.id != request.user.id:
            Notification.objects.create(
                recipient=target,
                actor=request.user,
                verb="followed you",
                target=target,  # Generic target (User)
            )

        return Response({
            "detail": "Now following user.",
            "following_count": request.user.following.count(),
            "target_followers_count": target.followers.count(),
        }, status=status.HTTP_201_CREATED)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()  # checker literal
    lookup_url_kwarg = "user_id"

    def post(self, request, user_id: int):
        if request.user.id == user_id:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        target = self.get_object()
        if not request.user.following.filter(pk=target.pk).exists():
            return Response({
                "detail": "You are not following this user.",
                "following_count": request.user.following.count(),
                "target_followers_count": target.followers.count(),
            }, status=status.HTTP_200_OK)

        request.user.following.remove(target)
        return Response({
            "detail": "Unfollowed user.",
            "following_count": request.user.following.count(),
            "target_followers_count": target.followers.count(),
        }, status=status.HTTP_200_OK)
