# Create a Book

```python
from bookshelf.models import Book

# Create the book "1984" by George Orwell (1949)
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# Expected output (id will vary):
# <Book: 1984 by George Orwell (1949)>

# Retrieve a Book

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

# Update a Book

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

# Delete a Book

## `delete.md`

```markdown
# Delete the Book and Confirm

```python
from bookshelf.models import Book

# Get and delete the updated book
b = Book.objects.get(title="Nineteen Eighty-Four", author="George Orwell", publication_year=1949)
b.delete()
# Expected output (row counts may vary):
# (1, {'bookshelf.Book': 1})

# Confirm no books remain
list(Book.objects.all())
# Expected output:
# []
