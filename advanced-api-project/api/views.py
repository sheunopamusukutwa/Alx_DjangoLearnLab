from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


# -----------------------------
# List all books (with filtering, searching, ordering)
# -----------------------------
class BookListView(generics.ListAPIView):
    """
    Retrieve a list of all Book instances.
    Supports filtering, searching, and ordering.
    Public read-only access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filter, search, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering by specific fields
    filterset_fields = ["title", "author", "publication_year"]

    # Searching (partial text match)
    search_fields = ["title", "author__name"]

    # Ordering (sort results)
    ordering_fields = ["title", "publication_year"]
    ordering = ["title"]  # Default ordering


# -----------------------------
# Retrieve single book (public, read-only)
# -----------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# -----------------------------
# Create book (authenticated only)
# -----------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Update book (authenticated only)
# -----------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Delete book (authenticated only)
# -----------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
