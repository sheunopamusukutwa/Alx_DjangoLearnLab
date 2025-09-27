from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from .models import Book, Library


# -------------------------
# BOOK LIST (requires view permission)
# -------------------------
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """List all books — requires can_view permission."""
    books = Book.objects.all()  # ORM = safe query (no SQL injection risk)
    return render(request, "bookshelf/book_list.html", {"books": books})


# -------------------------
# LIBRARY DETAIL VIEW
# -------------------------
class LibraryDetailView(DetailView):
    """Detail view for a single library."""
    model = Library
    template_name = "bookshelf/library_detail.html"
    context_object_name = "library"


# -------------------------
# USER REGISTRATION
# -------------------------
def register(request):
    """Register a new user and auto-login."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login
            return redirect("book_list")
    else:
        form = UserCreationForm()
    return render(request, "bookshelf/register.html", {"form": form})


# -------------------------
# ROLE DASHBOARDS
# -------------------------
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def admin_view(request):
    """Admin dashboard view — requires can_view permission."""
    return render(request, "bookshelf/admin_view.html")


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def librarian_view(request):
    """Librarian dashboard view — requires can_edit permission."""
    return render(request, "bookshelf/librarian_view.html")


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def member_view(request):
    """Member dashboard view — requires can_view permission."""
    return render(request, "bookshelf/member_view.html")


# -------------------------
# BOOK MANAGEMENT FORMS
# -------------------------
class BookForm(forms.ModelForm):
    """Form for creating and editing books."""
    class Meta:
        model = Book
        fields = ["title", "author"]


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    """Add a new book — requires can_create permission."""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/book_form.html", {"form": form, "action": "Add"})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    """Edit an existing book — requires can_edit permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/book_form.html", {"form": form, "action": "Edit"})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """Delete a book — requires can_delete permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "bookshelf/book_confirm_delete.html", {"book": book})
