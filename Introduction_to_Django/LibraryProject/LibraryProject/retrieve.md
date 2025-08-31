## `retrieve.md`

```markdown
# Retrieve the Book

```python
from bookshelf.models import Book

# Retrieve the book we just created
b = Book.objects.get(title="1984", author="George Orwell", publication_year=1949)

# Show all attributes
b.id, b.title, b.author, b.publication_year
# Expected output (id will vary):
# (1, '1984', 'George Orwell', 1949)
