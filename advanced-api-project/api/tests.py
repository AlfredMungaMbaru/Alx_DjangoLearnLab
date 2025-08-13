from django.test import TestCase
from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorModelTest(TestCase):
    """Test cases for the Author model."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
    
    def test_author_creation(self):
        """Test that an author can be created successfully."""
        self.assertEqual(self.author.name, "Test Author")
        self.assertEqual(str(self.author), "Test Author")
    
    def test_author_string_representation(self):
        """Test the string representation of the author."""
        self.assertEqual(str(self.author), "Test Author")


class BookModelTest(TestCase):
    """Test cases for the Book model."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
    
    def test_book_creation(self):
        """Test that a book can be created successfully."""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.publication_year, 2020)
        self.assertEqual(self.book.author, self.author)
    
    def test_book_string_representation(self):
        """Test the string representation of the book."""
        expected = "Test Book by Test Author (2020)"
        self.assertEqual(str(self.book), expected)
    
    def test_book_author_relationship(self):
        """Test the foreign key relationship between Book and Author."""
        # Test that the book is associated with the correct author
        self.assertEqual(self.book.author.name, "Test Author")
        
        # Test the reverse relationship (author.books)
        self.assertIn(self.book, self.author.books.all())


class BookSerializerTest(TestCase):
    """Test cases for the BookSerializer."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
    
    def test_book_serialization(self):
        """Test serializing a book instance."""
        serializer = BookSerializer(self.book)
        expected_data = {
            'id': self.book.id,
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        self.assertEqual(serializer.data, expected_data)
    
    def test_future_year_validation(self):
        """Test that future publication years are rejected."""
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.id
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)
    
    def test_valid_publication_year(self):
        """Test that valid publication years are accepted."""
        current_year = datetime.now().year
        data = {
            'title': 'Current Book',
            'publication_year': current_year,
            'author': self.author.id
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class AuthorSerializerTest(TestCase):
    """Test cases for the AuthorSerializer."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
        self.book1 = Book.objects.create(
            title="Book One",
            publication_year=2020,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            publication_year=2022,
            author=self.author
        )
    
    def test_author_serialization_with_books(self):
        """Test serializing an author with nested books."""
        serializer = AuthorSerializer(self.author)
        data = serializer.data
        
        # Check basic author data
        self.assertEqual(data['name'], 'Test Author')
        self.assertEqual(data['books_count'], 2)
        
        # Check nested books data
        self.assertEqual(len(data['books']), 2)
        book_titles = [book['title'] for book in data['books']]
        self.assertIn('Book One', book_titles)
        self.assertIn('Book Two', book_titles)
        
        # Check publication year range
        self.assertEqual(data['publication_year_range']['earliest'], 2020)
        self.assertEqual(data['publication_year_range']['latest'], 2022)
    
    def test_author_without_books(self):
        """Test serializing an author without any books."""
        author_no_books = Author.objects.create(name="No Books Author")
        serializer = AuthorSerializer(author_no_books)
        data = serializer.data
        
        self.assertEqual(data['name'], 'No Books Author')
        self.assertEqual(data['books_count'], 0)
        self.assertEqual(len(data['books']), 0)
        self.assertNotIn('publication_year_range', data)
