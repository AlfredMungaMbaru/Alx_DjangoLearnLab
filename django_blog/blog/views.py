from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post

# Create your views here.

def post_list(request):
    """Display a list of all published posts"""
    posts = Post.objects.all().order_by('-published_date')
    
    # Add pagination
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, post_id):
    """Display a single post"""
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)
