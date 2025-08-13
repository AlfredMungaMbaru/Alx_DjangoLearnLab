from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm

# Create your views here.

# Function-based views for authentication
def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            login(request, user)  # Automatically log in the user after registration
            return redirect('blog:post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view and edit"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('blog:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    # Get user's posts
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    
    context = {
        'form': form,
        'user_posts': user_posts
    }
    return render(request, 'blog/profile.html', context)

# Class-based views for blog post CRUD operations

class PostListView(ListView):
    """Display a paginated list of all blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = context['page_obj']
        return context

class PostDetailView(DetailView):
    """Display a single blog post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new blog post - requires authentication"""
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Set the author to the current user before saving"""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing blog post - only by the author"""
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Add success message when post is updated"""
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Ensure only the post author can edit the post"""
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a blog post - only by the author"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def delete(self, request, *args, **kwargs):
        """Add success message when post is deleted"""
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """Ensure only the post author can delete the post"""
        post = self.get_object()
        return self.request.user == post.author

# Legacy function-based views (kept for backward compatibility)
def post_list(request):
    """Display a list of all published posts - redirects to class-based view"""
    return redirect('blog:posts')

def post_detail(request, post_id):
    """Display a single post - redirects to class-based view"""
    return redirect('blog:post_detail', pk=post_id)
