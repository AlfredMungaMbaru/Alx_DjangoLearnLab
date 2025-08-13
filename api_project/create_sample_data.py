#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/home/munga/Desktop/Alx/Alx_DjangoLearnLab/api_project')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
django.setup()

from api.models import Book

# Create sample books
books_data = [
    {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
    {'title': '1984', 'author': 'George Orwell'},
    {'title': 'Pride and Prejudice', 'author': 'Jane Austen'},
    {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
    {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger'},
]

# Add books to database if they don't exist
for book_data in books_data:
    book, created = Book.objects.get_or_create(
        title=book_data['title'],
        defaults={'author': book_data['author']}
    )
    if created:
        print(f"Created book: {book.title} by {book.author}")
    else:
        print(f"Book already exists: {book.title}")

print(f"\nTotal books in database: {Book.objects.count()}")
