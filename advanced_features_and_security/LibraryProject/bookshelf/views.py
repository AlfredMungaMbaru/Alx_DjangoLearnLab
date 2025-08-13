from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Book
from .forms import BookForm


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books. Requires 'can_view' permission.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    View to display book details. Requires 'can_view' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


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
def book_search(request):
    """
    View to search books. Available to all logged-in users.
    """
    query = request.GET.get('q', '')
    books = []
    
    if query:
        if request.user.has_perm('bookshelf.can_view'):
            books = Book.objects.filter(
                title__icontains=query
            ) | Book.objects.filter(
                author__icontains=query
            )
        else:
            messages.error(request, "You don't have permission to search books.")
    
    return render(request, 'bookshelf/book_search.html', {
        'books': books,
        'query': query
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
