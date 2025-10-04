from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment, Tag


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class PostForm(forms.ModelForm):
    # NEW: free-text, comma-separated tags
    tag_names = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g. django, tips, how-to)",
        widget=forms.TextInput(attrs={"placeholder": "e.g. django, tips"}),
        label="Tags",
    )

    class Meta:
        model = Post
        fields = ("title", "content")  # author set in the view; published_date auto
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate tag_names when editing
        if self.instance and self.instance.pk:
            current = self.instance.tags.values_list("name", flat=True)
            self.fields["tag_names"].initial = ", ".join(current)

    def save(self, commit=True):
        # Save Post fields only; tags handled separately via save_tags()
        instance = super().save(commit=commit)
        self._post_instance = instance
        return instance

    def save_tags(self, post):
        raw = (self.cleaned_data.get("tag_names") or "").strip()
        names = [n.strip() for n in raw.split(",") if n.strip()]
        tag_objs = []
        for name in names:
            # normalize: title-case or lower? We'll keep the exact casing typed.
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)
        post.tags.set(tag_objs)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "placeholder": "Write a comment..."}),
        }

    def clean_content(self):
        content = (self.cleaned_data.get("content") or "").strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content
