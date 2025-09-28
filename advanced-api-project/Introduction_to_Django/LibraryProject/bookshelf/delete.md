## `delete.md`

```markdown
# Delete the Book and Confirm

```python
from bookshelf.models import Book

# Get and delete the updated book
book = Book.objects.get(title="Nineteen Eighty-Four", author="George Orwell", publication_year=1949)
book.delete()
# Expected output (row counts may vary):
# (1, {'bookshelf.Book': 1})

# Confirm no books remain
list(Book.objects.all())
# Expected output:
# []
