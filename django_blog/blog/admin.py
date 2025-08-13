from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new post
            obj.author = request.user
        super().save_model(request, obj, form, change)
