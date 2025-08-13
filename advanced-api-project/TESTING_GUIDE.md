# Django REST Framework API Testing Guide

## Overview

This document provides comprehensive information about the unit testing implementation for the Django REST Framework API in the `advanced_api_project`. The test suite ensures the integrity of API endpoints, validates response data, and verifies proper authentication and permission controls.

## Test Structure

### Test Files
- **`api/test_views.py`**: Main test file containing all API endpoint tests
- **`api/tests.py`**: Original model and serializer tests
- **Test Database**: Automatically created and destroyed by Django's test framework

### Test Categories

#### 1. Model Tests (`ModelTestCase`)
- **Purpose**: Test model creation, validation, and relationships
- **Coverage**: Author and Book model creation, string representations, foreign key relationships

#### 2. Book API CRUD Tests (`BookAPITestCase`)
- **Purpose**: Test all CRUD operations for Book endpoints
- **Coverage**: 
  - Create, read, update, delete operations
  - Authentication and permission validation
  - Data validation and error handling
  - Status code verification

#### 3. Filtering and Search Tests (`BookFilteringTestCase`)
- **Purpose**: Test filtering, searching, and ordering functionality
- **Coverage**:
  - Filter by author, author name, publication year
  - Range filtering for publication years
  - Search across title and author fields
  - Ordering by various fields
  - Combined filtering and ordering

#### 4. Author API Tests (`AuthorAPITestCase`)
- **Purpose**: Test Author endpoints and nested serialization
- **Coverage**:
  - Author listing with nested books
  - Author detail views
  - Author creation with authentication
  - Search functionality

#### 5. Pagination Tests (`PaginationTestCase`)
- **Purpose**: Test API pagination functionality
- **Coverage**:
  - First and subsequent pages
  - Page size limits
  - Navigation links (next/previous)

#### 6. Error Handling Tests (`ErrorHandlingTestCase`)
- **Purpose**: Test API error handling and edge cases
- **Coverage**:
  - Invalid data submission
  - Non-existent resource access
  - Invalid filter parameters
  - Malformed requests

#### 7. Serializer Tests (`SerializerTestCase`)
- **Purpose**: Test custom serializer validation and functionality
- **Coverage**:
  - BookSerializer validation (including future year validation)
  - AuthorSerializer nested serialization
  - Error message verification

## Test Data Setup

### Users
- **Test User**: Created for authentication testing
  - Username: `testuser`
  - Password: `testpass123`

### Test Authors
- **J.K. Rowling**: For Harry Potter books
- **George Orwell**: For 1984 and Animal Farm
- **Agatha Christie**: For mystery novels

### Test Books
- **Harry Potter series**: Multiple books for filtering tests
- **Classic literature**: 1984, Animal Farm for variety
- **Mystery novels**: For comprehensive coverage

## Running Tests

### Run All Tests
```bash
# Run all API tests
python manage.py test api.test_views

# Run with verbose output
python manage.py test api.test_views -v 2

# Run with coverage (if django-coverage is installed)
coverage run --source='.' manage.py test api.test_views
coverage report
```

### Run Specific Test Categories
```bash
# Run only CRUD tests
python manage.py test api.test_views.BookAPITestCase

# Run only filtering tests
python manage.py test api.test_views.BookFilteringTestCase

# Run only permission tests
python manage.py test api.test_views.BookAPITestCase.test_book_create_unauthenticated_fails

# Run multiple specific tests
python manage.py test api.test_views.BookAPITestCase.test_book_create_authenticated_success api.test_views.BookAPITestCase.test_book_update_authenticated_success
```

### Run Original Model Tests
```bash
# Run original model and serializer tests
python manage.py test api.tests
```

## Test Cases Documentation

### Authentication and Permission Tests

#### Unauthenticated Access
- ✅ **GET requests**: Should succeed for list and detail views
- ❌ **POST/PUT/PATCH/DELETE**: Should return 401 Unauthorized

#### Authenticated Access
- ✅ **All operations**: Should succeed with proper data
- ✅ **Data validation**: Should enforce serializer validation rules

### CRUD Operation Tests

#### Create (POST)
```python
def test_book_create_authenticated_success(self):
    """Test successful book creation with authentication."""
    # Expected: 201 Created, correct response data
    # Verifies: Database record creation, response format
```

#### Read (GET)
```python
def test_book_list_unauthenticated(self):
    """Test book list access without authentication."""
    # Expected: 200 OK, paginated results
    # Verifies: Public read access, data structure
```

#### Update (PUT/PATCH)
```python
def test_book_update_authenticated_success(self):
    """Test successful book update with authentication."""
    # Expected: 200 OK, updated data
    # Verifies: Database changes, response accuracy
```

#### Delete (DELETE)
```python
def test_book_delete_authenticated_success(self):
    """Test successful book deletion with authentication."""
    # Expected: 204 No Content, database removal
    # Verifies: Record deletion, proper status code
```

### Filtering and Search Tests

#### Filter by Author
```python
def test_filter_by_author(self):
    """Test filtering books by author ID."""
    # URL: /api/books/?author=1
    # Expected: Only books by specified author
```

#### Search Functionality
```python
def test_search_functionality(self):
    """Test search across multiple fields."""
    # URL: /api/books/?search=Harry
    # Expected: Books matching search term in title or author
```

#### Ordering Tests
```python
def test_ordering_by_publication_year_descending(self):
    """Test descending order by publication year."""
    # URL: /api/books/?ordering=-publication_year
    # Expected: Results ordered newest to oldest
```

### Validation Tests

#### Future Year Validation
```python
def test_book_create_future_year_validation(self):
    """Test rejection of future publication years."""
    # Input: publication_year = current_year + 1
    # Expected: 400 Bad Request, validation error
```

#### Required Field Validation
```python
def test_invalid_book_data(self):
    """Test handling of missing required fields."""
    # Input: Empty data or missing fields
    # Expected: 400 Bad Request, field-specific errors
```

## Response Format Verification

### Success Responses
```json
{
    "id": 1,
    "title": "Book Title",
    "publication_year": 2020,
    "author": 1
}
```

### Error Responses
```json
{
    "publication_year": [
        "Publication year cannot be in the future. Current year is 2025."
    ]
}
```

### Paginated Responses
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [...]
}
```

## Test Environment Configuration

### Database
- **Test Database**: Automatically created in memory or temporary file
- **Isolation**: Each test runs in a transaction that's rolled back
- **Data**: Fresh test data created for each test class

### Authentication
- **Test Client**: Uses APIClient for API requests
- **Force Authentication**: Uses `force_authenticate()` for authenticated tests
- **Session Management**: Automatic cleanup between tests

## Continuous Integration

### Pre-commit Testing
```bash
# Add to your pre-commit hooks
#!/bin/sh
echo "Running API tests..."
python manage.py test api.test_views --verbosity=1
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

### Coverage Requirements
- **Minimum Coverage**: 90% for API views
- **Critical Paths**: 100% coverage for CRUD operations
- **Edge Cases**: All error conditions tested

## Test Maintenance

### Adding New Tests
1. **Identify the feature**: What needs testing?
2. **Choose test class**: Model, API, filtering, etc.
3. **Set up data**: Create minimal required test data
4. **Write test**: Follow existing patterns
5. **Verify coverage**: Ensure new code is tested

### Test Data Management
- **Minimal Data**: Create only what's needed for each test
- **Isolation**: Don't rely on data from other tests
- **Cleanup**: Django handles database cleanup automatically

### Performance Considerations
- **Fast Tests**: Use in-memory database for speed
- **Selective Running**: Run only relevant tests during development
- **Parallel Execution**: Use `--parallel` flag for faster execution

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure Python path is correct
export PYTHONPATH=/path/to/project:$PYTHONPATH
python manage.py test api.test_views
```

#### Database Issues
```bash
# Reset test database
python manage.py migrate --run-syncdb
python manage.py test api.test_views
```

#### Permission Issues
```bash
# Check user creation in tests
# Verify force_authenticate() usage
# Confirm permission class configuration
```

### Debug Mode
```bash
# Run with debug output
python manage.py test api.test_views --debug-mode --verbosity=2

# Run specific failing test with debug
python manage.py test api.test_views.BookAPITestCase.test_book_create_authenticated_success --debug-mode
```

## Best Practices

### Test Writing
1. **Descriptive Names**: Test names should explain what they test
2. **Single Responsibility**: Each test should test one thing
3. **Arrange-Act-Assert**: Clear test structure
4. **Independence**: Tests should not depend on each other

### Data Management
1. **setUp() Method**: Create test data in setUp()
2. **Minimal Data**: Only create what's needed
3. **Realistic Data**: Use realistic but simple test data
4. **Avoid Fixtures**: Create data programmatically for clarity

### Assertions
1. **Specific Assertions**: Use appropriate assertion methods
2. **Status Codes**: Always verify HTTP status codes
3. **Response Data**: Check response content, not just status
4. **Database State**: Verify database changes when relevant

## Conclusion

This comprehensive test suite ensures that:
- ✅ All API endpoints work correctly
- ✅ Authentication and permissions are enforced
- ✅ Data validation works as expected
- ✅ Filtering, searching, and ordering function properly
- ✅ Error handling is robust
- ✅ Response formats are consistent

The tests provide confidence in the API's reliability and help catch regressions during development.
