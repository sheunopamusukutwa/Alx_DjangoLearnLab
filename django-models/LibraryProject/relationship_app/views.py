from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all()  # <- keeps the other required pattern
    return render(request, "relationship_app/list_books.html", {"books": books})
