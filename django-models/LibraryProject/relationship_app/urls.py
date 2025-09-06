from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views                                  # <-- required for "views.register"
from .views import list_books, LibraryDetailView

app_name = "relationship_app"

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Auth routes
    path("login/",  LoginView.as_view(template_name="relationship_app/login.html"),  name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),   # <-- EXACT: "views.register"
]
