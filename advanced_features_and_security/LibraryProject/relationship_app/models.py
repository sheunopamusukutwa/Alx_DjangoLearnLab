from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# -----------------------
# Custom User + Manager
# -----------------------
class CustomUserManager(BaseUserManager):
    """Manager for handling user creation with extra fields."""

    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    """Extend Django's default user with DOB & profile photo."""
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    profile_photo = models.ImageField(
        _("profile photo"),
        upload_to="profiles/",
        null=True,
        blank=True
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username


# -----------------------
# Domain Models
# -----------------------
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
        on_delete=models.CASCADE,
        related_name="books",
    )

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]
        # Custom permissions (in addition to Django’s built-ins add/change/delete/view)
        permissions = (
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        )

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
        on_delete=models.CASCADE,
        related_name="librarian",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} @ {self.library.name}"


# -----------------------
# Role-Based Access Profile
# -----------------------
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    def __str__(self):
        return f"{self.user.username} ({self.role})"