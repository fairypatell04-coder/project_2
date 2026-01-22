# posts/views.py
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from accounts.models import Profile
from .models import Post, Comment
from .forms import PostForm, CommentForm, CustomUserCreationForm, UserEditForm, ProfileEditForm


# ------------------------
# Custom Login View
# ------------------------
class CustomLoginView(LoginView):
    template_name = 'posts/registration/login.html'


# ------------------------
# Register View
# ------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('posts:feed')
    else:
        form = CustomUserCreationForm()
    return render(request, 'posts/registration/register.html', {'form': form})


# ------------------------
# Logout
# ------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('accounts:login')


# ------------------------
# Feed View
# ------------------------
class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


# ------------------------
# Post Detail
# ------------------------
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        ctx['comments'] = self.object.comments.all().order_by('-created_at')
        return ctx


# ------------------------
# Create Post
# ------------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)


# ------------------------
# Delete Post
# ------------------------
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:feed')

    def test_func(self):
        return self.get_object().author == self.request.user


# ------------------------
# Add Comment
# ------------------------
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added!")
    else:
            messages.error(request, "Invalid comment data!")
    return redirect(post.get_absolute_url())


# ------------------------
# Toggle Like
# ------------------------
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'total_likes': post.likes.count()})
    return redirect(post.get_absolute_url())
    


# ------------------------
# Profile View
# ------------------------
@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    return render(request, 'posts/profile.html', {'user_obj': user_obj})


# ------------------------
# Edit Profile
# ------------------------
@login_required
def edit_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    if request.user != user_obj:
        return redirect('posts:profile_view', username=request.user.username)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user_obj)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=user_obj.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated!")
            return redirect('posts:profile_view', username=user_obj.username)
    else:
        user_form = UserEditForm(instance=user_obj)
        profile_form = ProfileEditForm(instance=user_obj.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_obj': user_obj,
    }
    return render(request, 'accounts/profile_edit.html', context)
