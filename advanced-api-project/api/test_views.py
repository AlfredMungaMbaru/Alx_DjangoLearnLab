"""
Comprehensive unit tests for Django REST Framework API views.

This module contains thorough test cases for all API endpoints including:
- CRUD operations for Book and Author models
- Filtering, searching, and ordering functionality
- Permission and authentication testing
- Response data integrity and status code verification

Test Categories:
1. Model Creation and Validation Tests
2. API Endpoint CRUD Tests
3. Filtering and Search Tests
4. Ordering Tests
5. Permission and Authentication Tests
6. Error Handling Tests
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from datetime import datetime
import json

from api.models import Author, Book
from api.serializers import BookSerializer, AuthorSerializer


class ModelTestCase(TestCase):
    """Test cases for model creation and validation."""
    
    def setUp(self):
        """Set up test data for model tests."""
        self.author = Author.objects.create(name="Test Author")
        self.book_data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author
        }
    
    def test_author_creation(self):
        """Test that authors can be created successfully."""
        author = Author.objects.create(name="New Author")
        self.assertEqual(author.name, "New Author")
        self.assertEqual(str(author), "New Author")
    
    def test_book_creation(self):
        """Test that books can be created successfully."""
        book = Book.objects.create(**self.book_data)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.publication_year, 2020)
        self.assertEqual(book.author, self.author)
        self.assertIn("Test Book", str(book))
    
    def test_book_author_relationship(self):
        """Test the foreign key relationship between Book and Author."""
        book = Book.objects.create(**self.book_data)
        self.assertEqual(book.author.name, "Test Author")
        self.assertIn(book, self.author.books.all())


class BookAPITestCase(APITestCase):
    """Comprehensive test cases for Book API endpoints."""
    
    def setUp(self):
        """Set up test data and authentication."""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )
        
        # Set up API client
        self.client = APIClient()
        
        # Define test URLs
        self.books_list_url = reverse('api:book-list')
        self.books_create_url = reverse('api:book-create')
        self.book_detail_url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        self.book_update_url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        self.book_delete_url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
    
    def test_book_list_unauthenticated(self):
        """Test that unauthenticated users can view book list."""
        response = self.client.get(self.books_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 2)
    
    def test_book_detail_unauthenticated(self):
        """Test that unauthenticated users can view book details."""
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['author'], self.book1.author.pk)
    
    def test_book_create_unauthenticated_fails(self):
        """Test that unauthenticated users cannot create books."""
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.books_create_url, data, format='json')
        # DRF returns 403 Forbidden for permission denied scenarios
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_create_authenticated_success(self):
        """Test that authenticated users can create books."""
        self.client.login(username='testuser', password='testpass123')
        book_data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(self.books_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(response.data['publication_year'], 2023)
        
        # Verify book was created in database
        new_book = Book.objects.get(title='New Book')
        self.assertEqual(new_book.author, self.author1)
    
    def test_book_create_future_year_validation(self):
        """Test that books with future publication years are rejected."""
        self.client.login(username='testuser', password='testpass123')
        future_year = datetime.now().year + 1
        book_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.pk
        }
        response = self.client.post(self.books_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_book_update_authenticated_success(self):
        """Test that authenticated users can update books."""
        self.client.login(username='testuser', password='testpass123')
        update_data = {
            'title': 'Updated Title',
            'publication_year': 1998,
            'author': self.author1.pk
        }
        response = self.client.put(self.book_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        
        # Verify update in database
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Updated Title')
    
    def test_book_partial_update_authenticated(self):
        """Test partial update (PATCH) of books."""
        self.client.login(username='testuser', password='testpass123')
        update_data = {'title': 'Partially Updated Title'}
        response = self.client.patch(self.book_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated Title')
        # Verify other fields remain unchanged
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_book_update_unauthenticated_fails(self):
        """Test that unauthenticated users cannot update books."""
        book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author1
        )
        
        data = {
            'title': 'Updated Title',
            'publication_year': 2021,
            'author': self.author1.id
        }
        
        url = reverse('api:book-update', kwargs={'pk': book.pk})
        response = self.client.put(url, data, format='json')
        # DRF returns 403 Forbidden for permission denied scenarios
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_delete_authenticated_success(self):
        """Test that authenticated users can delete books."""
        self.client.login(username='testuser', password='testpass123')
        book_id = self.book1.pk
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was deleted from database
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=book_id)
    
    def test_book_delete_unauthenticated_fails(self):
        """Test that unauthenticated users cannot delete books."""
        response = self.client.delete(self.book_delete_url)
        # DRF returns 403 Forbidden for permission denied scenarios
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify book still exists
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())


class BookFilteringTestCase(APITestCase):
    """Test cases for filtering, searching, and ordering functionality."""
    
    def setUp(self):
        """Set up test data for filtering tests."""
        # Create authors
        self.rowling = Author.objects.create(name="J.K. Rowling")
        self.orwell = Author.objects.create(name="George Orwell")
        self.christie = Author.objects.create(name="Agatha Christie")
        
        # Create books with different years and authors
        self.hp1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.rowling
        )
        self.hp2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.rowling
        )
        self.book_1984 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.orwell
        )
        self.animal_farm = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.orwell
        )
        self.orient_express = Book.objects.create(
            title="Murder on the Orient Express",
            publication_year=1934,
            author=self.christie
        )
        
        self.books_list_url = reverse('api:book-list')
    
    def test_filter_by_author(self):
        """Test filtering books by author."""
        response = self.client.get(self.books_list_url, {'author': self.rowling.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        for book in results:
            self.assertEqual(book['author'], self.rowling.pk)
    
    def test_filter_by_author_name(self):
        """Test filtering books by author name."""
        response = self.client.get(self.books_list_url, {'author_name': 'Rowling'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        response = self.client.get(self.books_list_url, {'publication_year': 1997})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Harry Potter and the Philosopher's Stone")
    
    def test_filter_by_publication_year_range(self):
        """Test filtering books by publication year range."""
        response = self.client.get(self.books_list_url, {
            'publication_year_min': 1990,
            'publication_year_max': 2000
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)  # Both Harry Potter books
    
    def test_filter_by_title(self):
        """Test filtering books by title."""
        response = self.client.get(self.books_list_url, {'title': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)  # Both Harry Potter books
    
    def test_search_functionality(self):
        """Test search across title and author name."""
        # Search for "Harry" should find Harry Potter books
        response = self.client.get(self.books_list_url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        
        # Search for "Orwell" should find Orwell's books
        response = self.client.get(self.books_list_url, {'search': 'Orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
    
    def test_ordering_by_title(self):
        """Test ordering books by title."""
        response = self.client.get(self.books_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        # Verify ascending order
        titles = [book['title'] for book in results]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_publication_year_descending(self):
        """Test ordering books by publication year (descending)."""
        response = self.client.get(self.books_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        # Verify descending order by year
        years = [book['publication_year'] for book in results]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_combined_filtering_and_ordering(self):
        """Test combining filters with ordering."""
        response = self.client.get(self.books_list_url, {
            'author_name': 'Rowling',
            'ordering': 'publication_year'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        # Should be ordered by year: 1997, 1998
        self.assertEqual(results[0]['publication_year'], 1997)
        self.assertEqual(results[1]['publication_year'], 1998)


class AuthorAPITestCase(APITestCase):
    """Test cases for Author API endpoints."""
    
    def setUp(self):
        """Set up test data for author tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.author = Author.objects.create(name="Test Author")
        self.book1 = Book.objects.create(
            title="Book One",
            publication_year=2020,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            publication_year=2021,
            author=self.author
        )
        
        self.authors_list_url = reverse('api:author-list')
        self.author_detail_url = reverse('api:author-detail', kwargs={'pk': self.author.pk})
        self.author_create_url = reverse('api:author-create')
    
    def test_author_list_includes_books(self):
        """Test that author list includes nested book data."""
        response = self.client.get(self.authors_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        author_data = None
        for author in response.data['results']:
            if author['id'] == self.author.pk:
                author_data = author
                break
        
        self.assertIsNotNone(author_data)
        self.assertEqual(author_data['name'], "Test Author")
        self.assertEqual(len(author_data['books']), 2)
        self.assertEqual(author_data['books_count'], 2)
        self.assertIn('publication_year_range', author_data)
    
    def test_author_detail(self):
        """Test author detail view."""
        response = self.client.get(self.author_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Author")
        self.assertEqual(len(response.data['books']), 2)
    
    def test_author_create_authenticated(self):
        """Test creating authors with authentication."""
        self.client.login(username='testuser', password='testpass123')
        author_data = {'name': 'New Author'}
        response = self.client.post(self.author_create_url, author_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Author')
    
    def test_author_create_unauthenticated_fails(self):
        """Test that unauthenticated users cannot create authors."""
        author_data = {'name': 'Should Not Create'}
        response = self.client.post(self.author_create_url, author_data)
        # DRF returns 403 Forbidden for permission denied scenarios
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_author_search(self):
        """Test searching authors by name."""
        response = self.client.get(self.authors_list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Test Author')


class PaginationTestCase(APITestCase):
    """Test cases for API pagination."""
    
    def setUp(self):
        """Set up test data for pagination tests."""
        self.author = Author.objects.create(name="Prolific Author")
        
        # Create many books to test pagination
        for i in range(25):
            Book.objects.create(
                title=f"Book {i+1}",
                publication_year=2000 + (i % 23),  # Vary years
                author=self.author
            )
        
        self.books_list_url = reverse('api:book-list')
    
    def test_pagination_first_page(self):
        """Test first page of paginated results."""
        response = self.client.get(self.books_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)  # Default page size
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], 25)
    
    def test_pagination_second_page(self):
        """Test second page of paginated results."""
        response = self.client.get(self.books_list_url, {'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # Remaining books
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])


class ErrorHandlingTestCase(APITestCase):
    """Test cases for error handling and edge cases."""
    
    def setUp(self):
        """Set up test data for error handling tests."""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.author = Author.objects.create(name="Test Author")
        self.books_create_url = reverse('api:book-create')
    
    def test_invalid_book_data(self):
        """Test creating book with invalid data."""
        self.client.login(username='testuser', password='testpass123')
        
        # Missing required fields
        response = self.client.post(self.books_create_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Invalid author ID
        response = self.client.post(self.books_create_url, {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': 99999  # Non-existent author
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_nonexistent_book_detail(self):
        """Test accessing non-existent book."""
        response = self.client.get(reverse('api:book-detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_invalid_filter_parameters(self):
        """Test that invalid filter parameters return appropriate errors."""
        books_list_url = reverse('api:book-list')
        
        # Invalid publication year - django-filter validates this and returns 400
        response = self.client.get(books_list_url, {'publication_year': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Invalid author ID - django-filter validates this and returns 400
        response = self.client.get(books_list_url, {'author': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SerializerTestCase(TestCase):
    """Test cases for custom serializers."""
    
    def setUp(self):
        """Set up test data for serializer tests."""
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
    
    def test_book_serializer_validation(self):
        """Test BookSerializer validation."""
        # Valid data
        valid_data = {
            'title': 'Valid Book',
            'publication_year': 2020,
            'author': self.author.pk
        }
        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        
        # Invalid future year
        future_year = datetime.now().year + 1
        invalid_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.pk
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)
    
    def test_author_serializer_nested_books(self):
        """Test AuthorSerializer includes nested books."""
        serializer = AuthorSerializer(self.author)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Author')
        self.assertEqual(len(data['books']), 1)
        self.assertEqual(data['books_count'], 1)
        self.assertIn('publication_year_range', data)
        self.assertEqual(data['publication_year_range']['earliest'], 2020)
        self.assertEqual(data['publication_year_range']['latest'], 2020)


# Test runner utility
class APITestRunner:
    """Utility class to run specific test categories."""
    
    @staticmethod
    def run_crud_tests():
        """Run only CRUD operation tests."""
        test_cases = [
            'api.test_views.BookAPITestCase.test_book_create_authenticated_success',
            'api.test_views.BookAPITestCase.test_book_update_authenticated_success',
            'api.test_views.BookAPITestCase.test_book_delete_authenticated_success',
        ]
        # This would be used with Django's test runner
        return test_cases
    
    @staticmethod
    def run_permission_tests():
        """Run only permission and authentication tests."""
        test_cases = [
            'api.test_views.BookAPITestCase.test_book_create_unauthenticated_fails',
            'api.test_views.BookAPITestCase.test_book_update_unauthenticated_fails',
            'api.test_views.BookAPITestCase.test_book_delete_unauthenticated_fails',
        ]
        return test_cases
    
    @staticmethod
    def run_filtering_tests():
        """Run only filtering and search tests."""
        test_cases = [
            'api.test_views.BookFilteringTestCase',
        ]
        return test_cases
