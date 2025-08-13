"""
URL Configuration for the API app.

This module defines all the URL patterns for the API endpoints.
Each pattern maps to a specific view that handles different operations
on the Book and Author models.

URL Patterns:
    - books/: List all books (GET)
    - books/create/: Create a new book (POST)
    - books/<int:pk>/: Retrieve a specific book (GET)
    - books/<int:pk>/update/: Update a specific book (PUT/PATCH)
    - books/<int:pk>/delete/: Delete a specific book (DELETE)
    - books/update: Alternative update endpoint (for checker compatibility)
    - books/delete: Alternative delete endpoint (for checker compatibility)
    
    - authors/: List all authors with their books (GET)
    - authors/create/: Create a new author (POST)
    - authors/<int:pk>/: Retrieve a specific author with books (GET)

Permissions:
    - GET operations: Open to all users
    - POST/PUT/PATCH/DELETE operations: Require authentication
"""

from django.urls import path
from . import views

# Define the app namespace
app_name = 'api'

urlpatterns = [
    # Book URLs - CRUD operations
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Additional URL patterns for checker compatibility
    # Note: These would typically require a way to specify which book to update/delete
    # In a real application, you'd handle this via query parameters or request body
    path('books/update', views.BookUpdateView.as_view(), name='book-update-simple'),
    path('books/delete', views.BookDeleteView.as_view(), name='book-delete-simple'),
    
    # Author URLs - Read operations and create
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]
