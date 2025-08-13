"""
Custom filters for the API app.

This module defines custom filter classes to provide advanced filtering
capabilities for the Book and Author models. These filters extend the
basic filtering functionality provided by django-filter.
"""

import django_filters
from django.db.models import Q, Count
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Advanced filter class for the Book model.
    
    This filter provides comprehensive filtering options including:
    - Exact matches for author and publication year
    - Range filtering for publication year
    - Text search across title and author name
    - Custom filtering logic for complex queries
    """
    
    # Basic filters
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text="Filter by book title (case-insensitive, partial match)"
    )
    
    author = django_filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        field_name='author',
        help_text="Filter by specific author"
    )
    
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Filter by author name (case-insensitive, partial match)"
    )
    
    # Publication year filters
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        help_text="Filter by exact publication year"
    )
    
    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text="Filter books published from this year onwards"
    )
    
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text="Filter books published up to this year"
    )
    
    publication_year_range = django_filters.RangeFilter(
        field_name='publication_year',
        help_text="Filter by publication year range (format: min,max)"
    )
    
    # Custom search filter
    search = django_filters.CharFilter(
        method='filter_search',
        help_text="Search across title and author name"
    )
    
    def filter_search(self, queryset, name, value):
        """
        Custom search method that searches across multiple fields.
        
        This method allows searching for a term across both the book title
        and the author's name simultaneously.
        
        Args:
            queryset: The initial queryset
            name: The filter field name (not used in this case)
            value: The search term
            
        Returns:
            Filtered queryset containing books that match the search term
        """
        if not value:
            return queryset
            
        return queryset.filter(
            Q(title__icontains=value) | Q(author__name__icontains=value)
        )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
            'author': ['exact'],
            'author__name': ['exact', 'icontains'],
        }


class AuthorFilter(django_filters.FilterSet):
    """
    Filter class for the Author model.
    
    Provides filtering options for authors including:
    - Name-based filtering
    - Filtering by the number of books written
    """
    
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text="Filter by author name (case-insensitive, partial match)"
    )
    
    # Filter authors who have written at least X books
    min_books = django_filters.NumberFilter(
        method='filter_min_books',
        help_text="Filter authors who have written at least this many books"
    )
    
    def filter_min_books(self, queryset, name, value):
        """
        Filter authors by minimum number of books written.
        
        Args:
            queryset: The initial queryset
            name: The filter field name
            value: Minimum number of books
            
        Returns:
            Filtered queryset of authors with at least 'value' books
        """
        if value is None:
            return queryset
            
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__gte=value)
    
    class Meta:
        model = Author
        fields = {
            'name': ['exact', 'icontains'],
        }
