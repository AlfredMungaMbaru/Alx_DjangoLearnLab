from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from taggit.models import Tag
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm, CommentForm, SearchForm

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
        context['search_form'] = SearchForm()
        # Add popular tags (tags with most posts)
        context['popular_tags'] = Tag.objects.filter(taggit_taggeditem_items__isnull=False).distinct()[:10]
        return context

class PostDetailView(DetailView):
    """Display a single blog post with comments"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Add comments and comment form to context"""
        context = super().get_context_data(**kwargs)
        # Get all comments for this post, ordered by creation date
        context['comments'] = self.object.comments.all().order_by('created_at')
        # Add comment form for authenticated users
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context

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


# Comment Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    """Create a new comment for a specific post"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Set the comment author and associated post"""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        messages.success(self.request, 'Your comment has been added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the post detail page after creating comment"""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        """Add the post to context"""
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing comment"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Add success message when comment is updated"""
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the post detail page after updating comment"""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        """Ensure only the comment author can edit the comment"""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_context_data(self, **kwargs):
        """Add the post to context"""
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        context['is_edit'] = True
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment"""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        """Add success message when comment is deleted"""
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        """Redirect to the post detail page after deleting comment"""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        """Ensure only the comment author can delete the comment"""
        comment = self.get_object()
        return self.request.user == comment.author


# Search and Tag Views
def search_posts(request):
    """Search posts by title, content, or tags"""
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Search in title, content, and tags
            results = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
    
    return render(request, 'blog/search_results.html', {
        'form': form,
        'query': query,
        'results': results
    })


class PostsByTagView(ListView):
    """Display posts filtered by a specific tag"""
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Filter posts by tag name"""
        self.tag = get_object_or_404(Tag, name=self.kwargs['tag_name'])
        return Post.objects.filter(tags=self.tag)
    
    def get_context_data(self, **kwargs):
        """Add tag to context"""
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class TagListView(ListView):
    """Display all available tags"""
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
    
    def get_queryset(self):
        """Get tags that have at least one post"""
        return Tag.objects.filter(taggit_taggeditem_items__isnull=False).distinct().order_by('name')
