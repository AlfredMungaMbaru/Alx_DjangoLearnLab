from django.contrib import admin
from .models import Book, Library, Membership, BookReview


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model.
    Demonstrates how to work with models that reference the custom user model.
    """
    list_display = ['title', 'author', 'owner', 'publication_date', 'created_at']
    list_filter = ['publication_date', 'created_at', 'owner']
    search_fields = ['title', 'author', 'isbn']
    ordering = ['-created_at']
    
    # Show the custom user fields in the filter
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('owner')


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Library model.
    """
    list_display = ['name', 'location', 'member_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'location']
    # Cannot use filter_horizontal with through model
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Number of Members'


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """
    Admin configuration for Membership model.
    """
    list_display = ['user', 'library', 'membership_type', 'joined_date', 'is_active']
    list_filter = ['membership_type', 'is_active', 'joined_date']
    search_fields = ['user__username', 'user__email', 'library__name']
    ordering = ['-joined_date']


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for BookReview model.
    """
    list_display = ['book', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'reviewer__username', 'review_text']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('book', 'reviewer')
