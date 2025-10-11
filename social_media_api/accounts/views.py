from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

# Create your views here.

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    POST /accounts/register/
    Creates a new user and returns a token in the response.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]  # allow image upload


class LoginView(APIView):
    """
    POST /accounts/login/
    Returns a token if credentials are valid.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /accounts/profile/  -> current user's details
    PUT/PATCH /accounts/profile/ -> update bio/profile_picture/email, etc.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user