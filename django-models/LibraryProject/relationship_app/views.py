from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login   
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from .models import Library  

# FBV: list all books (keeps required substrings)
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# CBV: library detail (keeps required substrings)
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# Registration view: use built-in form + login() to sign in immediately
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)                 # <-- use the imported login
            return redirect("list_books")        # or your preferred landing page
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

# helpers to check roles
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'

def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

def member_view(request):
    return render(request, "relationship_app/member_view.html")

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'

# --- REQUIRED role-restricted views ---

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")