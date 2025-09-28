from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# -----------------------------
# ListView (all books)
# -----------------------------
class BookListView(generics.ListAPIView):
    """
    Retrieve a list of all Book instances.
    Accessible to everyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------
# DetailView (single book by ID)
# -----------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single Book by ID.
    Accessible to everyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------
# CreateView (add new book)
# -----------------------------
class BookCreateView(generics.CreateAPIView):
    """
    Create a new Book instance.
    Only accessible to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
# UpdateView (modify book)
# -----------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing Book instance.
    Only accessible to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
# DeleteView (remove book)
# -----------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    Delete an existing Book instance.
    Only accessible to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
