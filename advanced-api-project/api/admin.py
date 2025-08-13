from django.contrib import admin
from .models import Author, Book

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin configuration for Author model."""
    list_display = ['name', 'books_count']
    search_fields = ['name']
    ordering = ['name']
    
    def books_count(self, obj):
        """Return the number of books by this author."""
        return obj.books.count()
    books_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model."""
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering = ['title']
    
    # Display author name in dropdown for easier selection
    autocomplete_fields = ['author']
