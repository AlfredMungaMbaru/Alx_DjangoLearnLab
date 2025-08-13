# Django Permissions and Groups Implementation

## Project Overview

This Django project demonstrates a comprehensive implementation of Django's permissions and groups system for managing user access to book-related operations. The system provides granular access control through custom permissions and user groups.

## Features Implemented

### 1. Custom User Model
- Extended Django's `AbstractUser` with additional fields
- `date_of_birth`: DateField for user's birth date
- `profile_photo`: ImageField for profile pictures
- Custom user manager with `create_user` and `create_superuser` methods

### 2. Custom Permissions System
The Book model includes four custom permissions:
- `can_view`: Permission to view books
- `can_create`: Permission to create new books
- `can_edit`: Permission to edit existing books
- `can_delete`: Permission to delete books

### 3. User Groups
Three predefined groups with different permission levels:

#### Viewers Group
- **Permissions**: `can_view`
- **Access**: Read-only access to books
- **Use Case**: Regular users who need to browse books

#### Editors Group
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Access**: Can view, create, and modify books
- **Use Case**: Content creators and moderators

#### Admins Group
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Access**: Full access to all book operations
- **Use Case**: System administrators

## Project Structure

```
LibraryProject/
├── bookshelf/                  # Main application
│   ├── models.py              # Custom User and Book models with permissions
│   ├── views.py               # Permission-protected views
│   ├── admin.py               # Django admin configuration
│   ├── forms.py               # Book forms for CRUD operations
│   ├── urls.py                # URL routing
│   ├── templates/             # HTML templates
│   │   └── bookshelf/
│   │       ├── base.html      # Base template with permission checks
│   │       ├── book_list.html # Book listing with conditional UI
│   │       └── book_form.html # Create/edit book form
│   └── management/            # Custom management commands
│       └── commands/
│           ├── setup_groups.py    # Create groups and permissions
│           └── create_test_users.py # Create test users
├── LibraryProject/            # Project settings
│   └── settings.py            # Django settings with AUTH_USER_MODEL
├── README.md                  # This file
└── PERMISSIONS_GUIDE.md       # Detailed implementation guide
```

## Installation and Setup

### 1. Prerequisites
- Python 3.8+
- Django 4.0+
- Pillow (for ImageField support)

### 2. Initial Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django pillow

# Apply migrations
python manage.py makemigrations
python manage.py migrate
```

### 3. Set Up Groups and Permissions
```bash
# Create user groups and assign permissions
python manage.py setup_groups

# Create test users for testing
python manage.py create_test_users
```

### 4. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## Usage and Testing

### Test User Accounts
The `create_test_users` command creates these test accounts:

| Username | Password | Group | Permissions |
|----------|----------|-------|-------------|
| viewer_user | testpass123 | Viewers | can_view |
| editor_user | testpass123 | Editors | can_view, can_create, can_edit |
| admin_user | testpass123 | Admins | can_view, can_create, can_edit, can_delete |

### Testing Scenarios

1. **Viewer Access Test**
   - Login as `viewer_user`
   - Should see books but no create/edit/delete buttons
   - Cannot access protected URLs like `/bookshelf/book/create/`
   - Should receive 403 Forbidden for unauthorized actions

2. **Editor Access Test**
   - Login as `editor_user`
   - Can view, create, and edit books
   - Cannot delete books (no delete button/access)
   - Can access create and edit URLs

3. **Admin Access Test**
   - Login as `admin_user`
   - Full access to all book operations
   - Can view, create, edit, and delete books
   - Access to all protected URLs

### Available URLs

- **Book List**: `/bookshelf/` (requires `can_view`)
- **Create Book**: `/bookshelf/book/create/` (requires `can_create`)
- **Edit Book**: `/bookshelf/book/<id>/edit/` (requires `can_edit`)
- **Delete Book**: `/bookshelf/book/<id>/delete/` (requires `can_delete`)
- **Search Books**: `/bookshelf/search/` (requires `can_view`)
- **Django Admin**: `/admin/`

## Implementation Details

### Permission Enforcement in Views

#### Function-Based Views
```python
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
```

#### Class-Based Views
```python
class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'bookshelf.can_create'
    # ... rest of implementation
```

### Template-Level Permission Checks
```html
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}">Create New Book</a>
{% endif %}
```

### Model Permissions Definition
```python
class Book(models.Model):
    # ... model fields ...
    
    class Meta:
        permissions = [
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ]
```

## Security Features

### Multi-Layer Security
1. **Authentication**: All views require login
2. **Authorization**: Permission decorators on views
3. **Template Security**: UI elements hidden based on permissions
4. **URL Protection**: Direct URL access blocked without permissions

### Error Handling
- **403 Forbidden**: Displayed when users lack required permissions
- **Login Redirect**: Unauthenticated users redirected to login page
- **User Feedback**: Clear messages about permission requirements

## Management Commands

### setup_groups.py
Creates user groups and assigns permissions automatically.

```bash
python manage.py setup_groups
```

### create_test_users.py
Creates test users and assigns them to different groups for testing.

```bash
python manage.py create_test_users
```

## Admin Interface

The Django admin interface includes:
- Custom user admin with additional fields
- Group management with permission assignments
- User-to-group assignment interface
- Permission management tools

Access admin at: `http://127.0.0.1:8000/admin/`

## Troubleshooting

### Common Issues

1. **Permissions Not Working**
   - Ensure migrations are applied: `python manage.py migrate`
   - Run setup command: `python manage.py setup_groups`

2. **Users Can't Access Features**
   - Check user group assignments in Django admin
   - Verify group permissions are correctly set

3. **403 Forbidden Errors**
   - Expected behavior for users without required permissions
   - Check user's group membership and permissions

### Debug Commands
```bash
# Check user permissions
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(username='test_user')
>>> user.get_all_permissions()

# List all permissions
>>> from django.contrib.auth.models import Permission
>>> Permission.objects.filter(content_type__app_label='bookshelf')
```

## Documentation

For detailed implementation information, see:
- `PERMISSIONS_GUIDE.md` - Comprehensive implementation guide
- Code comments throughout the project
- Django official documentation on permissions

## License

This project is for educational purposes demonstrating Django permissions and groups implementation.

## Contributing

This is a demonstration project for learning Django permissions. Feel free to use it as a reference for your own implementations.
