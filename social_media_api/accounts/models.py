from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

def profile_upload_to(instance, filename):
    # media/profiles/<username>/<filename>
    return f"profiles/{instance.username}/{filename}"

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=profile_upload_to, blank=True, null=True)

    # Directed graph: who follows this user (followers) and who this user follows (following via related_name)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.username