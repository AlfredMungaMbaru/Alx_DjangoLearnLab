# Custom User Model Implementation

This Django project demonstrates the implementation of a custom user model that extends Django's `AbstractUser` class with additional fields and functionality.

## Project Structure

```
advanced_features_and_security/
├── accounts/                    # Custom user model app
│   ├── models.py               # Custom user model and manager
│   ├── admin.py                # Admin configuration for custom user
│   └── migrations/
├── bookshelf/                  # Example app using custom user model
│   ├── models.py               # Models with foreign keys to custom user
│   ├── admin.py                # Admin for bookshelf models
│   └── migrations/
├── advanced_features_and_security/  # Project settings
│   ├── settings.py             # AUTH_USER_MODEL configuration
│   └── urls.py                 # URL configuration with media files
└── manage.py
```

## Implementation Details

### 1. Custom User Model (`accounts/models.py`)

The `CustomUser` model extends Django's `AbstractUser` and adds:
- `date_of_birth`: DateField for storing user's birth date
- `profile_photo`: ImageField for user profile pictures
- Custom properties like `age` calculation
- Helper methods like `get_profile_photo_url()`

### 2. Custom User Manager (`accounts/models.py`)

The `CustomUserManager` handles:
- `create_user()`: Creates regular users with proper field handling
- `create_superuser()`: Creates admin users with required permissions

### 3. Settings Configuration (`settings.py`)

Key configurations:
- `AUTH_USER_MODEL = 'accounts.CustomUser'`: Points to our custom model
- Media file handling for profile photos
- App registration

### 4. Admin Integration (`accounts/admin.py`)

Custom admin features:
- Extended fieldsets with new fields
- Profile photo preview in list view
- Age calculation display
- Custom form validation

### 5. Model Relationships (`bookshelf/models.py`)

Demonstrates proper usage of custom user model:
- Foreign key relationships using `settings.AUTH_USER_MODEL`
- Many-to-many relationships through intermediate models
- Proper related names and reverse relationships

## Key Features

1. **Backwards Compatibility**: Uses `settings.AUTH_USER_MODEL` for all references
2. **Admin Integration**: Full Django admin support with custom configurations
3. **Media Handling**: Proper image upload and serving configuration
4. **Relationship Management**: Examples of various relationship types
5. **Data Validation**: Custom validation and helper methods

## Usage Examples

### Creating Users
```python
from accounts.models import CustomUser

# Create regular user
user = CustomUser.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password',
    date_of_birth='1990-01-01'
)

# Create superuser
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin_password'
)
```

### Accessing Custom Fields
```python
user = CustomUser.objects.get(username='john_doe')
print(f"User age: {user.age}")
print(f"Profile photo URL: {user.get_profile_photo_url()}")
```

### Foreign Key Relationships
```python
from bookshelf.models import Book

# Create a book owned by the user
book = Book.objects.create(
    title='Django Mastery',
    author='Expert Author',
    isbn='1234567890123',
    publication_date='2023-01-01',
    owner=user
)

# Access user's books
user_books = user.books.all()
```

## Migration Notes

1. Create initial migrations: `python manage.py makemigrations`
2. Apply migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`

## Dependencies

- Django 5.2.5
- Pillow (for ImageField support)

This implementation provides a solid foundation for applications requiring extended user functionality while maintaining Django's built-in authentication features.
