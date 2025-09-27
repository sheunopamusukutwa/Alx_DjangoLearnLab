from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import book_list, LibraryDetailView

app_name = "bookshelf"

urlpatterns = [
    path("books/", book_list, name="book_list"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Role-based views
    path("roles/admin/", views.admin_view, name="admin_view"),
    path("roles/librarian/", views.librarian_view, name="librarian_view"),
    path("roles/member/", views.member_view, name="member_view"),

    # Auth
    path("login/", LoginView.as_view(template_name="bookshelf/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="bookshelf/logout.html"), name="logout"),
    path("register/", views.register, name="register"),

    # Book management
    path("add_book/", views.add_book, name="add_book"),
    path("edit_book/<int:pk>/", views.edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", views.delete_book, name="delete_book"),
]