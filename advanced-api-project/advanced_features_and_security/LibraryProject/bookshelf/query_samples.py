"""
Query samples for bookshelf.

Usage options:
1) python manage.py shell < bookshelf/query_samples.py
2) DJANGO_SETTINGS_MODULE=<project>.settings python bookshelf/query_samples.py
"""

import os
import sys

# If run directly (not via manage.py shell), try to bootstrap Django.
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    # EDIT this to your actual project package if running as a standalone script.
    # Example: os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
    pass

try:
    import django  # type: ignore
    django.setup()
except Exception:
    # If manage.py shell is piping this file, Django is already set up; ignore.
    pass

from LibraryProject.bookshelf.models import Author, Book, Library, Librarian

def get_books_by_author(author_name: str):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author) 

def get_books_in_library(library_name: str):
    library = Library.objects.get(name=library_name)
    return library.books.all()                 

def get_librarian_for_library(library_name: str):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library) 

