"""
Query samples for relationship_app.

Usage options:
1) python manage.py shell < relationship_app/query_samples.py
2) DJANGO_SETTINGS_MODULE=<project>.settings python relationship_app/query_samples.py
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

from relationship_app.models import Author, Book, Library, Librarian  # noqa: E402


# 1) Query all books by a specific author.
def get_books_by_author(author_name: str):
    """
    Returns a QuerySet of Book objects for the given author name.
    """
    return Book.objects.select_related("author").filter(author__name=author_name)


# 2) List all books in a library.
def get_books_in_library(library_name: str):
    """
    Returns a distinct QuerySet of Book objects that belong to the named Library.
    """
    return (
        Book.objects.select_related("author")
        .filter(libraries__name=library_name)
        .distinct()
    )


# 3) Retrieve the librarian for a library.
def get_librarian_for_library(library_name: str):
    """
    Returns the Librarian instance (or None) responsible for the named Library.
    """
    return Librarian.objects.select_related("library").filter(
        library__name=library_name
    ).first()


# Optional: small demo to show output if you run this file directly.
if __name__ == "__main__":
    author_name = "Chinua Achebe"
    library_name = "Downtown Library"

    print(f"\nBooks by author: {author_name}")
    for b in get_books_by_author(author_name):
        print(f"- {b.title} ({b.author.name})")

    print(f"\nBooks in library: {library_name}")
    for b in get_books_in_library(library_name):
        print(f"- {b.title} ({b.author.name})")

    print(f"\nLibrarian for library: {library_name}")
    libn = get_librarian_for_library(library_name)
    print(f"- {libn.name}" if libn else "- None found")
