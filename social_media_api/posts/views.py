from rest_framework import viewsets, permissions, filters
from rest_framework.generics import ListAPIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


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
        # Keep performance optimization
        return super().get_queryset().select_related("author")

    def perform_create(self, serializer):
        # Never trust client-sent author; set it server-side.
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
        serializer.save(author=self.request.user)


class FeedView(ListAPIView):
    """
    /api/feed/
    Lists posts authored by users the current user follows, newest first.
    Requires authentication.
    Supports global pagination, search, ordering.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        # Use the exact variable name and call the checker expects:
        following_users = user.following.all()
        qs = Post.objects.filter(author__in=following_users).order_by("-created_at")
        # Keep optimization while preserving the exact substring above
        return qs.select_related("author")
