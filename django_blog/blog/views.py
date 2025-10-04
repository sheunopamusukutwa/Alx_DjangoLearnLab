from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import RegisterForm, ProfileForm, PostForm, CommentForm
from .models import Post, Comment, Tag


# ---- Public pages ----
def home(request):
    return render(request, "blog/home.html")


# ---- Auth ----
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "registration/profile.html", {"form": form})


# ---- Posts CRUD ----
class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # Save tags after post exists
        form.save_tags(self.object)
        messages.success(self.request, "Post created successfully.")
        return response

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save_tags(self.object)
        messages.success(self.request, "Post updated successfully.")
        return response

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted.")
        return super().delete(request, *args, **kwargs)


# ---- Comments (from Task 3) ----
class CommentListView(ListView):
    model = Comment
    context_object_name = "comments"
    template_name = "blog/comment_list.html"

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_id"]).select_related("author", "post")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["post"] = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return ctx


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id") or kwargs.get("pk")
        self.post_obj = get_object_or_404(Post, pk=post_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.post_obj
        form.instance.author = self.request.user
        messages.success(self.request, "Comment added.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.post_obj.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["post"] = self.post_obj
        return ctx


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs["pk"])

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["post"] = self.object.post
        return ctx


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs["pk"])

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})


# ---- Tags ----
class TagPostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/tag_post_list.html"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        # Support either /tags/<slug:tag_slug>/ or /tags/<str:tag_name>/
        slug = kwargs.get("tag_slug")
        name = kwargs.get("tag_name")
        if slug:
            self.tag = get_object_or_404(Tag, slug=slug)
        elif name:
            self.tag = get_object_or_404(Tag, name=name)
        else:
            self.tag = None
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if not self.tag:
            return Post.objects.none()
        return Post.objects.filter(tags=self.tag).select_related("author").prefetch_related("tags")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag"] = self.tag
        return ctx


# ---- Search ----
class SearchResultsView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/search_results.html"
    paginate_by = 10

    def get_queryset(self):
        q = (self.request.GET.get("q") or "").strip()
        if not q:
            return Post.objects.none()
        return (
            Post.objects.filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(tags__name__icontains=q)
            )
            .select_related("author")
            .prefetch_related("tags")
            .distinct()
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("q", "")
        return ctx
