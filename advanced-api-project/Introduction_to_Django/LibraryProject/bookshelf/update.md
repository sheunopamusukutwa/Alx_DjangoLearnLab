## `update.md`

```markdown
# Update the Book Title

```python
from bookshelf.models import Book

# Get the existing book and update its title
book = Book.objects.get(title="1984", author="George Orwell", publication_year=1949)
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm the update
Book.objects.get(id=b.id).title
# Expected output:
# 'Nineteen Eighty-Four'
