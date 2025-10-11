from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source="author.id", read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author_id",
            "author_username",
            "title",
            "content",
            "created_at",
            "updated_at",
            "comments_count",
        ]
        read_only_fields = [
            "id",
            "author_id",
            "author_username",
            "created_at",
            "updated_at",
            "comments_count",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source="author.id", read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "content",
            "author_id",
            "author_username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author_id", "author_username", "created_at", "updated_at"]

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        return value