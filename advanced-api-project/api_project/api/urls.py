from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Router for CRUD ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Existing ListAPIView endpoint
    path("books/", BookList.as_view(), name="book-list"),

    # Router URLs for full CRUD
    path("", include(router.urls)),
]