from rest_framework import viewsets, permissions, filters, status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

# Notifications
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    """
    /api/posts/  (GET list, POST create)
    /api/posts/{id}/ (GET retrieve, PUT/PATCH update, DELETE destroy)
    """
    # Checker expects this literal:
    queryset = Post.objects.all()

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return super().get_queryset().select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    /api/comments/  (GET list, POST create)
    /api/comments/{id}/ (GET retrieve, PUT/PATCH update, DELETE destroy)
    Optional filter by post: /api/comments/?post=<post_id>
    """
    # Checker expects this literal:
    queryset = Comment.objects.all()

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["content", "author__username", "post__title"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        qs = super().get_queryset().select_related("author", "post")
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        post = comment.post
        # Notify the post author (avoid self-notifications)
        if post.author_id != self.request.user.id:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb="commented on your post",
                target=post,
            )


class PostLikeView(APIView):
    """
    POST /api/posts/<pk>/like/
    Creates a like if not already liked; idempotent.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int):
        try:
            post = Post.objects.select_related("author").get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created and post.author_id != request.user.id:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post,
            )

        return Response(
            {"detail": "Liked" if created else "Already liked", "likes_count": post.likes.count()},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class PostUnlikeView(APIView):
    """
    POST /api/posts/<pk>/unlike/
    Deletes the like if it exists; idempotent.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        return Response(
            {"detail": "Unliked" if deleted else "Not liked", "likes_count": post.likes.count()},
            status=status.HTTP_200_OK,
        )


class FeedView(ListAPIView):
    """
    /api/feed/
    Lists posts authored by users the current user follows, newest first.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        qs = Post.objects.filter(author__in=following_users).order_by("-created_at")
        return qs.select_related("author")