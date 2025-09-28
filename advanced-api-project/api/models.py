from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Represents an author.
    One Author can have many Books (one-to-many relationship).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book linked to an Author.
    Each Book belongs to exactly one Author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name="books",   # Allows reverse lookup: author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"