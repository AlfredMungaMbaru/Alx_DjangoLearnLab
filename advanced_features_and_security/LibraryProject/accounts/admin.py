from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser


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


# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
