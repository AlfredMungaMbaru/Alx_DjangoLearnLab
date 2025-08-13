from django.shortcuts import render
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# Create your views here.

class BookListView(generics.ListAPIView):
    """
    Generic view for listing all books.
    
    This view provides read-only access to all Book instances in the database.
    It supports filtering, searching, and ordering capabilities.
    
    Permissions:
        - Read access is available to all users (authenticated and unauthenticated)
    
    Features:
        - Filtering by author and publication year
        - Search functionality across title and author name
        - Ordering by title, publication_year, and author name
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow read access to everyone
    
    # Add filtering, searching, and ordering capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering


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
    Generic view for listing all authors with their books.
    
    This view provides read-only access to all Author instances with nested books.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
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
