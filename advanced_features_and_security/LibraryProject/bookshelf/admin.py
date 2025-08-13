from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Book, Library, Membership, BookReview


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.
    Extends Django's UserAdmin to include our additional fields.
    """
    
    # Define the fields to be used in displaying the User model
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'age', 'profile_photo_preview', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    # Add the custom fields to the form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    
    # Add custom fields to the add form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    
    # Make certain fields read-only
    readonly_fields = ('date_joined', 'last_login')
    
    def profile_photo_preview(self, obj):
        """
        Display a small preview of the profile photo in the admin list view.
        """
        if obj.profile_photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.profile_photo.url
            )
        return "No Photo"
    profile_photo_preview.short_description = 'Profile Photo'
    
    def age(self, obj):
        """
        Display the calculated age in the admin list view.
        """
        return obj.age if obj.age is not None else "Not Set"
    age.short_description = 'Age'
    
    # Customize the admin change form
    def get_form(self, request, obj=None, **kwargs):
        """
        Override to customize the form behavior if needed.
        """
        form = super().get_form(request, obj, **kwargs)
        
        # You can add custom form validation or field modifications here
        if 'date_of_birth' in form.base_fields:
            form.base_fields['date_of_birth'].help_text = "Select the user's date of birth"
        
        if 'profile_photo' in form.base_fields:
            form.base_fields['profile_photo'].help_text = "Upload a profile photo (recommended size: 200x200px)"
        
        return form


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


# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
