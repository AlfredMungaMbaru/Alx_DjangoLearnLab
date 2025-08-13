from django.shortcuts import render
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .filters import BookFilter, AuthorFilter

# Create your views here.

class BookListView(generics.ListAPIView):
    """
    Enhanced generic view for listing all books with comprehensive filtering, searching, and ordering.
    
    This view provides read-only access to all Book instances in the database with advanced
    query capabilities including:
    
    Filtering Options:
        - title: Filter by book title (case-insensitive, partial match)
        - author: Filter by specific author ID
        - author_name: Filter by author name (case-insensitive, partial match)
        - publication_year: Filter by exact publication year
        - publication_year_min: Filter books published from this year onwards
        - publication_year_max: Filter books published up to this year
        - publication_year_range: Filter by publication year range (format: min,max)
        - search: Search across title and author name
    
    Search Functionality:
        - Searches across book title and author name simultaneously
        - Case-insensitive partial matching
        - Use 'search' parameter in query string
    
    Ordering Options:
        - title: Order by book title
        - publication_year: Order by publication year
        - author__name: Order by author name
        - Use 'ordering' parameter with optional '-' prefix for descending order
    
    Example API Calls:
        - GET /api/books/ - List all books
        - GET /api/books/?author=1 - Filter by author ID 1
        - GET /api/books/?search=Harry - Search for "Harry" in title or author
        - GET /api/books/?publication_year_min=2000 - Books from 2000 onwards
        - GET /api/books/?ordering=-publication_year - Order by year, newest first
        - GET /api/books/?author_name=Rowling&ordering=title - Books by authors with "Rowling" in name, ordered by title
    
    Permissions:
        - Read access is available to all users (authenticated and unauthenticated)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow read access to everyone
    
    # Configure filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Use custom filter class for advanced filtering
    filterset_class = BookFilter
    
    # Configure search functionality
    search_fields = ['title', 'author__name']  # Fields to search across
    
    # Configure ordering options
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    ordering = ['title']  # Default ordering
    
    def get_queryset(self):
        """
        Override get_queryset to add custom query optimizations.
        
        This method ensures that related objects are efficiently loaded
        and provides a hook for additional custom filtering logic.
        """
        queryset = super().get_queryset()
        
        # Optimize query with select_related to avoid N+1 queries
        queryset = queryset.select_related('author')
        
        # Add any additional custom filtering logic here if needed
        # For example, you could filter based on user permissions
        
        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic view for retrieving a single book by ID.
    
    This view provides read-only access to a specific Book instance.
    
    Permissions:
        - Read access is available to all users (authenticated and unauthenticated)
    
    URL Parameter:
        - pk: Primary key (ID) of the book to retrieve
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow read access to everyone


class BookCreateView(generics.CreateAPIView):
    """
    Generic view for creating a new book.
    
    This view handles the creation of new Book instances with proper validation.
    Only authenticated users can create new books.
    
    Permissions:
        - Write access restricted to authenticated users only
    
    Validation:
        - All BookSerializer validations apply (including future year validation)
        - Author must exist in the database
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_create(self, serializer):
        """
        Custom create method to add additional logic if needed.
        
        This method is called when a new book is being created.
        It can be used to set additional fields or perform custom actions.
        """
        # Save the book instance
        book = serializer.save()
        
        # Log the creation (in a real application, you might use proper logging)
        print(f"New book created: {book.title} by {book.author.name}")


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic view for updating an existing book.
    
    This view handles both partial (PATCH) and full (PUT) updates of Book instances.
    Only authenticated users can update books.
    
    Permissions:
        - Write access restricted to authenticated users only
    
    Validation:
        - All BookSerializer validations apply
        - Author must exist if being updated
    
    HTTP Methods:
        - PUT: Full update (all fields required)
        - PATCH: Partial update (only provided fields updated)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_update(self, serializer):
        """
        Custom update method to add additional logic if needed.
        
        This method is called when a book is being updated.
        It can be used to perform custom actions or logging.
        """
        book = serializer.save()
        print(f"Book updated: {book.title} by {book.author.name}")


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic view for deleting a book.
    
    This view handles the deletion of Book instances.
    Only authenticated users can delete books.
    
    Permissions:
        - Delete access restricted to authenticated users only
    
    URL Parameter:
        - pk: Primary key (ID) of the book to delete
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_destroy(self, instance):
        """
        Custom delete method to add additional logic if needed.
        
        This method is called when a book is being deleted.
        It can be used to perform cleanup or logging.
        """
        print(f"Book deleted: {instance.title} by {instance.author.name}")
        instance.delete()


# Combined CRUD View (Alternative approach using a single ViewSet)
class BookViewSet(generics.GenericAPIView):
    """
    Alternative combined view that demonstrates how to handle multiple operations
    in a single view class. This is not used in the URL patterns but serves as
    an educational example.
    
    Note: In practice, you would typically use separate views (as implemented above)
    or Django REST Framework's ViewSets for this functionality.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions required for this view.
        
        Different permissions based on the HTTP method:
        - GET: Allow anyone
        - POST, PUT, PATCH, DELETE: Require authentication
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]


# Additional views for Author model (bonus implementation)
class AuthorListView(generics.ListAPIView):
    """
    Enhanced generic view for listing all authors with comprehensive filtering and searching.
    
    This view provides read-only access to all Author instances with nested books
    and includes advanced query capabilities:
    
    Filtering Options:
        - name: Filter by author name (case-insensitive, partial match)
        - min_books: Filter authors who have written at least this many books
    
    Search Functionality:
        - Searches across author names
        - Case-insensitive partial matching
        - Use 'search' parameter in query string
    
    Ordering Options:
        - name: Order by author name
        - Use 'ordering' parameter with optional '-' prefix for descending order
    
    Example API Calls:
        - GET /api/authors/ - List all authors
        - GET /api/authors/?search=Rowling - Search for authors with "Rowling" in name
        - GET /api/authors/?min_books=2 - Authors with at least 2 books
        - GET /api/authors/?ordering=-name - Order by name, Z to A
    
    Permissions:
        - Read access is available to all users
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    
    # Configure filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Use custom filter class for advanced filtering
    filterset_class = AuthorFilter
    
    # Configure search functionality
    search_fields = ['name']
    
    # Configure ordering options
    ordering_fields = ['name', 'id']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """
    Generic view for retrieving a single author with their books.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


class AuthorCreateView(generics.CreateAPIView):
    """
    Generic view for creating a new author.
    
    Only authenticated users can create authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
