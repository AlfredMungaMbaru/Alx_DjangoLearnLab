from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from .models import Book
from .serializers import BookSerializer

# Custom permission class
class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the object.
        # Note: This would require adding an 'owner' field to the Book model
        # return obj.owner == request.user
        
        # For now, we'll allow all authenticated users to modify
        return request.user and request.user.is_authenticated

# Create your views here.

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of books.
    Only authenticated users can access this view.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    
    Permissions:
    - Read operations (GET): Available to authenticated users
    - Write operations (POST, PUT, DELETE): Restricted to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
