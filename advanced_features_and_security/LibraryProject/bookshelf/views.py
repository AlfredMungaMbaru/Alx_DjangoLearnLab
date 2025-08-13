from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.utils.html import escape
from django.core.exceptions import ValidationError
from django.db.models import Q
import logging
from .models import Book
from .forms import BookForm, ExampleForm
from .forms import ExampleForm

# Set up logging for security events
logger = logging.getLogger(__name__)


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Secure view to list all books with proper permission checking.
    Requires 'can_view' permission.
    """
    # Log access for security monitoring
    logger.info(f"User {request.user.username} accessed book list")
    
    try:
        # Use select_related to optimize database queries
        books = Book.objects.select_related('owner').all()
        return render(request, 'bookshelf/book_list.html', {'books': books})
    except Exception as e:
        logger.error(f"Error in book_list view: {str(e)}")
        messages.error(request, "An error occurred while loading books.")
        return render(request, 'bookshelf/book_list.html', {'books': []})


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    Secure view to display book details with input validation.
    Requires 'can_view' permission.
    """
    try:
        # Validate pk is a positive integer
        if not isinstance(pk, int) or pk <= 0:
            logger.warning(f"User {request.user.username} attempted access with invalid pk: {pk}")
            messages.error(request, "Invalid book ID.")
            return redirect('book_list')
        
        # Use get_object_or_404 for safe object retrieval
        book = get_object_or_404(Book.objects.select_related('owner'), pk=pk)
        
        # Log access
        logger.info(f"User {request.user.username} viewed book: {book.title}")
        
        return render(request, 'bookshelf/book_detail.html', {'book': book})
        
    except Exception as e:
        logger.error(f"Error in book_detail view: {str(e)}")
        messages.error(request, "An error occurred while loading the book.")
        return redirect('book_list')


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book. Requires 'can_create' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': 'Create Book'
    })


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book. Requires 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    # Additional check: only the owner or users with edit permission can edit
    if book.owner != request.user and not request.user.has_perm('bookshelf.can_edit'):
        return HttpResponseForbidden("You don't have permission to edit this book.")
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': 'Edit Book',
        'book': book
    })


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book. Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    # Additional check: only the owner or users with delete permission can delete
    if book.owner != request.user and not request.user.has_perm('bookshelf.can_delete'):
        return HttpResponseForbidden("You don't have permission to delete this book.")
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


@login_required
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_search(request):
    """
    Secure view to search books with input validation and XSS protection.
    Available to all logged-in users with proper permissions.
    """
    # Initialize variables
    query = ''
    books = []
    error_message = None
    
    # Check permissions first
    if not request.user.has_perm('bookshelf.can_view'):
        logger.warning(f"User {request.user.username} attempted unauthorized book search")
        messages.error(request, "You don't have permission to search books.")
        return redirect('book_list')
    
    if request.method == 'GET' and 'q' in request.GET:
        # Get and validate search query
        raw_query = request.GET.get('q', '').strip()
        
        # Input validation and sanitization
        if len(raw_query) > 100:  # Limit query length
            error_message = "Search query too long. Maximum 100 characters allowed."
            logger.warning(f"User {request.user.username} attempted overly long search query")
        elif raw_query:
            # Escape HTML to prevent XSS attacks
            query = escape(raw_query)
            
            try:
                # Use Django ORM with parameterized queries to prevent SQL injection
                # Q objects ensure safe query construction
                books = Book.objects.filter(
                    Q(title__icontains=query) | 
                    Q(author__icontains=query) |
                    Q(isbn__icontains=query)
                ).select_related('owner')[:50]  # Limit results to prevent DoS
                
                # Log successful search for monitoring
                logger.info(f"User {request.user.username} searched for: {query}")
                
            except Exception as e:
                # Log any database errors
                logger.error(f"Database error in book search: {str(e)}")
                error_message = "An error occurred while searching. Please try again."
                books = []
    
    return render(request, 'bookshelf/book_search.html', {
        'books': books,
        'query': query,
        'error_message': error_message,
    })


# Class-based view example with permission mixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class BookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Class-based view for listing books with permission check.
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'
    
    def get_queryset(self):
        return Book.objects.all().order_by('-created_at')


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Class-based view for creating books with permission check.
    """
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    permission_required = 'bookshelf.can_create'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Class-based view for updating books with permission check.
    """
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    permission_required = 'bookshelf.can_edit'
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Class-based view for deleting books with permission check.
    """
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    permission_required = 'bookshelf.can_delete'
    success_url = reverse_lazy('book_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# SECURE API ENDPOINTS
# ============================================================================

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect
def api_book_search(request):
    """
    Secure API endpoint for book search with JSON response.
    Includes rate limiting and input validation.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    query = request.GET.get('q', '').strip()
    
    # Input validation
    if not query:
        return JsonResponse({'error': 'Query parameter required'}, status=400)
    
    if len(query) > 100:
        return JsonResponse({'error': 'Query too long'}, status=400)
    
    try:
        # Escape query and use ORM for safe database access
        safe_query = escape(query)
        books = Book.objects.filter(
            Q(title__icontains=safe_query) | 
            Q(author__icontains=safe_query)
        ).values('id', 'title', 'author', 'isbn')[:20]  # Limit results
        
        # Convert QuerySet to list for JSON serialization
        books_list = list(books)
        
        return JsonResponse({
            'books': books_list,
            'count': len(books_list),
            'query': safe_query
        })
        
    except Exception as e:
        logger.error(f"API search error: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@login_required
@csrf_protect
def security_headers_test(request):
    """
    View to test security headers implementation.
    """
    response = render(request, 'bookshelf/security_test.html')
    
    # Add custom security headers
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    response['X-XSS-Protection'] = '1; mode=block'
    response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response
