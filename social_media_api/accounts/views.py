from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    Creates a new user and returns a token in the response.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]


class LoginView(APIView):
    """
    POST /api/accounts/login/
    Returns a token if credentials are valid.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/accounts/profile/  -> current user's details
    PUT/PATCH /api/accounts/profile/ -> update bio/profile_picture/email, etc.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user


class FollowUserView(APIView):
    """
    POST /api/accounts/follow/<user_id>/
    Current user follows the target user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int):
        if request.user.id == user_id:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Target user not found."}, status=status.HTTP_404_NOT_FOUND)

        # Already following?
        if request.user.following.filter(pk=target.pk).exists():
            return Response({
                "detail": "You are already following this user.",
                "following_count": request.user.following.count(),
                "target_followers_count": target.followers.count(),
            }, status=status.HTTP_200_OK)

        # Using the reverse manager created by related_name='following'
        request.user.following.add(target)

        return Response({
            "detail": "Now following user.",
            "following_count": request.user.following.count(),
            "target_followers_count": target.followers.count(),
        }, status=status.HTTP_201_CREATED)


class UnfollowUserView(APIView):
    """
    POST /api/accounts/unfollow/<user_id>/
    Current user unfollows the target user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int):
        if request.user.id == user_id:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Target user not found."}, status=status.HTTP_404_NOT_FOUND)

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
