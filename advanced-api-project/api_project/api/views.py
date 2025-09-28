from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer


# List view – only authenticated users can access
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# CRUD ViewSet – only authenticated users can access
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    Provides CRUD: list, retrieve, create, update, delete
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    """
Authentication & Permissions:
- All API endpoints require authentication.
- Token-based authentication is enabled.
- Obtain a token at /api/token/ by POSTing username/password.
- Include the token in requests: Authorization: Token <your_token>.
"""