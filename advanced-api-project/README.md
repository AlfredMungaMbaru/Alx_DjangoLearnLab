# Django REST Framework API Documentation

## Project Overview

This Django project implements a comprehensive API using Django REST Framework (DRF) with custom serializers and generic views. The API manages books and authors with full CRUD operations and advanced features like filtering, searching, and permissions.

## Project Structure

```
advanced-api-project/
├── advanced_api_project/
│   ├── settings.py          # Django settings with DRF configuration
│   ├── urls.py              # Main URL configuration
│   └── ...
├── api/
│   ├── models.py            # Author and Book models
│   ├── serializers.py       # Custom serializers with validation
│   ├── views.py             # Generic views for API endpoints
│   ├── urls.py              # API URL patterns
│   ├── admin.py             # Django admin configuration
│   └── tests.py             # Comprehensive test suite
├── manage.py
└── README.md
```

## Models

### Author Model
- `name`: CharField - The author's full name
- One-to-many relationship with Book model
- Related name: 'books'

### Book Model
- `title`: CharField - The book's title
- `publication_year`: IntegerField - Year of publication
- `author`: ForeignKey to Author - The book's author
- Custom validation: Publication year cannot be in the future

## API Endpoints

### Book Endpoints

| Method | URL | Description | Authentication Required |
|--------|-----|-------------|-------------------------|
| GET | `/api/books/` | List all books | No |
| POST | `/api/books/create/` | Create a new book | Yes |
| GET | `/api/books/<id>/` | Get specific book | No |
| PUT/PATCH | `/api/books/<id>/update/` | Update specific book | Yes |
| DELETE | `/api/books/<id>/delete/` | Delete specific book | Yes |
| PUT/PATCH | `/api/books/update` | Alternative update endpoint | Yes |
| DELETE | `/api/books/delete` | Alternative delete endpoint | Yes |

### Author Endpoints

| Method | URL | Description | Authentication Required |
|--------|-----|-------------|-------------------------|
| GET | `/api/authors/` | List all authors with books | No |
| POST | `/api/authors/create/` | Create a new author | Yes |
| GET | `/api/authors/<id>/` | Get specific author with books | No |

## Features

### 1. Generic Views
The API uses Django REST Framework's generic views for efficient CRUD operations:
- `ListAPIView` for listing resources
- `RetrieveAPIView` for getting single resources
- `CreateAPIView` for creating new resources
- `UpdateAPIView` for updating existing resources
- `DestroyAPIView` for deleting resources

### 2. Custom Serializers
- **BookSerializer**: Includes custom validation for publication year
- **AuthorSerializer**: Features nested serialization of related books
- Automatic book count and publication year range calculation for authors

### 3. Permissions
- **Read operations** (GET): Open to all users
- **Write operations** (POST, PUT, PATCH, DELETE): Require authentication
- Configured using DRF's permission classes

### 4. Filtering and Searching
- **Filtering**: By author and publication year
- **Searching**: Across book titles and author names
- **Ordering**: By title, publication year, and author name
- Uses `django-filter` package for advanced filtering capabilities

### 5. Data Validation
- Publication year cannot be in the future
- Author must exist when creating/updating books
- All standard Django model validations apply

## Configuration Details

### Django REST Framework Settings
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

### Custom View Behavior

#### BookCreateView
- Restricted to authenticated users
- Includes custom `perform_create` method for additional logic
- Validates all book data including publication year

#### BookUpdateView
- Supports both PUT (full update) and PATCH (partial update)
- Restricted to authenticated users
- Includes custom `perform_update` method

#### BookDeleteView
- Restricted to authenticated users
- Includes custom `perform_destroy` method for cleanup

#### AuthorSerializer Advanced Features
- Nested book serialization
- Automatic book count calculation
- Publication year range calculation
- Custom `to_representation` method for enhanced data

## Testing

### Manual Testing
1. **Start the development server**: `python manage.py runserver`
2. **Test endpoints** using curl, Postman, or the browsable API
3. **Verify permissions** by testing with and without authentication

### Example API Calls

#### List Books
```bash
curl -X GET "http://127.0.0.1:8000/api/books/"
```

#### Create Book (requires authentication)
```bash
curl -X POST "http://127.0.0.1:8000/api/books/create/" \
  -H "Content-Type: application/json" \
  -u "username:password" \
  -d '{
    "title": "New Book",
    "publication_year": 2023,
    "author": 1
  }'
```

#### Filter Books by Author
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?author=1"
```

#### Search Books
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?search=Harry"
```

### Automated Testing
Run the comprehensive test suite:
```bash
python manage.py test api
```

The test suite covers:
- Model creation and relationships
- Serializer validation
- View permissions
- CRUD operations
- Custom validation logic

## Security Considerations

1. **Authentication**: Uses session and basic authentication
2. **Permissions**: Read-only access for unauthenticated users
3. **Validation**: Custom validation prevents invalid data
4. **CSRF Protection**: Enabled for state-changing operations

## Production Considerations

1. **Database**: Currently uses SQLite; consider PostgreSQL for production
2. **Authentication**: Consider token-based authentication for APIs
3. **Permissions**: May need more granular permissions based on user roles
4. **Caching**: Consider adding caching for frequently accessed data
5. **Rate Limiting**: Add rate limiting to prevent abuse

## URL Pattern Design

The API follows RESTful conventions with additional patterns for compatibility:

1. **Standard RESTful patterns**: Use resource IDs in URLs
2. **Alternative patterns**: Simple paths without IDs for specific requirements
3. **Namespace**: All API endpoints are prefixed with `/api/`
4. **Named URLs**: All patterns have descriptive names for reverse URL resolution

This design provides flexibility while maintaining RESTful principles and meeting specific requirements for URL pattern checking.
