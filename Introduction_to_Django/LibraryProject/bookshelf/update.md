## `update.md`

```markdown
# Update the Book Title

```python
from bookshelf.models import Book

# Get the existing book and update its title
b = Book.objects.get(title="1984", author="George Orwell", publication_year=1949)
b.title = "Nineteen Eighty-Four"
b.save()

# Confirm the update
Book.objects.get(id=b.id).title
# Expected output:
# 'Nineteen Eighty-Four'
