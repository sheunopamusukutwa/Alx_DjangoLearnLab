from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    # ForeignKey → one Author has many Books
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,            # if an Author is deleted, delete their Books
        related_name="books",
    )

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} — {self.author.name}"


class Library(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # ManyToMany → a Library has many Books; a Book can live in many Libraries
    books = models.ManyToManyField(
        Book,
        related_name="libraries",
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=255)
    # OneToOne → each Library has exactly one Librarian (and vice versa)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,            # delete Librarian when Library is deleted
        related_name="librarian",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} @ {self.library.name}"
    
    class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    class Meta:
        # Custom permissions (in addition to Django’s built-ins add/change/delete/view)
        permissions = (
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        )

    def __str__(self):
        return f"{self.title} — {self.author.name}"