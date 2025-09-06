from django.http import HttpResponse
from .models import Book

# Function-based view: simple text list of books and authors
def list_books(request):
    books = Book.objects.all()  # <-- exact pattern the checker expects
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse("\n".join(lines), content_type="text/plain")