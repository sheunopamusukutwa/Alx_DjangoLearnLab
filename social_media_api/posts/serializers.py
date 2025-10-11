from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment, Like

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source="author.id", read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

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
            "likes_count",
        ]
        read_only_fields = [
            "id",
            "author_id",
            "author_username",
            "created_at",
            "updated_at",
            "comments_count",
            "likes_count",
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


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
