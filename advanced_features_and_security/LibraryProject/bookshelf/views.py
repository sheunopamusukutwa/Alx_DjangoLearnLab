from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from .models import Book, Library


# FBV: list all books
@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """List all books (requires can_view_book permission)."""
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


# CBV: library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = "bookshelf/library_detail.html"
    context_object_name = "library"


# Registration view: use built-in form + login() to sign in immediately
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect("book_list")
    else:
        form = UserCreationForm()
    return render(request, "bookshelf/register.html", {"form": form})


# --- ROLE-BASED VIEWS (restricted by group permissions) ---

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def admin_view(request):
    """Admin dashboard view — only accessible with view permission."""
    return render(request, "bookshelf/admin_view.html")


@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def librarian_view(request):
    """Librarian dashboard view — requires edit permission."""
    return render(request, "bookshelf/librarian_view.html")


@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def member_view(request):
    """Member dashboard view — requires view permission."""
    return render(request, "bookshelf/member_view.html")


# --- BOOK FORMS (restricted by permissions) ---

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author"]


@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def add_book(request):
    """Add a new book — requires can_create_book permission."""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/book_form.html", {"form": form, "action": "Add"})


@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, pk):
    """Edit an existing book — requires can_edit_book permission."""
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
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """Delete a book — requires can_delete_book permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "bookshelf/book_confirm_delete.html", {"book": book})