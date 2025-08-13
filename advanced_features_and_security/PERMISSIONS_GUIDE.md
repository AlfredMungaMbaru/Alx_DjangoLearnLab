# Django Permissions and Groups Implementation Guide

## Overview
This implementation demonstrates a comprehensive permissions and groups system for managing access to book-related operations in a Django application. The system uses Django's built-in authentication framework with custom permissions to control user access to different features.

## Custom Permissions Implemented

### Book Model Permissions
Located in `bookshelf/models.py`, the Book model includes these custom permissions:

```python
class Meta:
    permissions = [
        ('can_view', 'Can view book'),
        ('can_create', 'Can create book'),
        ('can_edit', 'Can edit book'),
        ('can_delete', 'Can delete book'),
    ]
```

## User Groups Configuration

### Groups and Their Permissions

1. **Viewers Group**
   - Permissions: `can_view`
   - Access Level: Can only view books and search
   - Use Case: Regular users who need read-only access

2. **Editors Group**
   - Permissions: `can_view`, `can_create`, `can_edit`
   - Access Level: Can view, create, and modify books
   - Use Case: Content creators and moderators

3. **Admins Group**
   - Permissions: `can_view`, `can_create`, `can_edit`, `can_delete`
   - Access Level: Full access to all book operations
   - Use Case: System administrators and super users

## Implementation Details

### Views with Permission Enforcement

All views in `bookshelf/views.py` implement permission checking using:

#### Function-Based Views
```python
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # View implementation
```

#### Class-Based Views
```python
class BookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bookshelf.can_view'
    # View implementation
```

### Permission Checks in Templates

Templates use Django's permission system to conditionally display UI elements:

```html
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}">Add Book</a>
{% endif %}
```

## Setup and Configuration

### 1. Automatic Setup
Run the management command to automatically create groups and assign permissions:

```bash
python manage.py setup_groups
```

This command will:
- Create the three user groups (Viewers, Editors, Admins)
- Assign appropriate permissions to each group
- Display a summary of the configuration

### 2. Manual Setup via Django Admin

1. **Access Django Admin**: Navigate to `/admin/`
2. **Create Groups**: Go to Authentication and Authorization > Groups
3. **Assign Permissions**: For each group, select the appropriate permissions
4. **Assign Users to Groups**: Edit users and add them to the desired groups

### 3. Testing the Implementation

#### Create Test Users
1. Create test users via Django admin or using `createsuperuser`
2. Assign each user to different groups
3. Test access by logging in as each user

#### Verification Steps
1. **Viewer Test**: Login as a Viewer, verify you can only see books
2. **Editor Test**: Login as an Editor, verify you can create and edit books
3. **Admin Test**: Login as an Admin, verify you can perform all operations

## URL Configuration

The application includes these protected endpoints:

- `/bookshelf/` - Book list (requires `can_view`)
- `/bookshelf/book/create/` - Create book (requires `can_create`)
- `/bookshelf/book/<id>/edit/` - Edit book (requires `can_edit`)
- `/bookshelf/book/<id>/delete/` - Delete book (requires `can_delete`)
- `/bookshelf/search/` - Search books (requires `can_view`)

## Security Features

### Multi-Level Protection
1. **Login Required**: All views require authentication
2. **Permission Required**: Each view checks for specific permissions
3. **Ownership Checks**: Additional checks for user ownership where applicable
4. **Template-Level Security**: UI elements hidden based on permissions

### Error Handling
- **403 Forbidden**: Raised when users lack required permissions
- **Login Redirect**: Unauthenticated users redirected to login
- **User-Friendly Messages**: Clear feedback about permission requirements

## File Structure

```
bookshelf/
├── models.py                     # Book model with custom permissions
├── views.py                      # Views with permission decorators
├── forms.py                      # Book form for create/edit operations
├── urls.py                       # URL patterns for book operations
├── admin.py                      # Admin configuration
├── management/
│   └── commands/
│       └── setup_groups.py       # Command to create groups and permissions
└── templates/
    └── bookshelf/
        ├── base.html             # Base template with permission checks
        ├── book_list.html        # Book listing with conditional UI
        └── book_form.html        # Create/edit form
```

## Usage Examples

### Checking Permissions in Views
```python
# Method 1: Using decorators
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    # View logic
    pass

# Method 2: Programmatic check
if request.user.has_perm('bookshelf.can_edit'):
    # Allow operation
    pass
else:
    # Deny operation
    return HttpResponseForbidden()
```

### Template Permission Checks
```html
<!-- Show create button only to users with create permission -->
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}">Create New Book</a>
{% endif %}

<!-- Display user's permissions -->
<ul>
    <li>View: {% if perms.bookshelf.can_view %}✓{% else %}✗{% endif %}</li>
    <li>Create: {% if perms.bookshelf.can_create %}✓{% else %}✗{% endif %}</li>
    <li>Edit: {% if perms.bookshelf.can_edit %}✓{% else %}✗{% endif %}</li>
    <li>Delete: {% if perms.bookshelf.can_delete %}✓{% else %}✗{% endif %}</li>
</ul>
```

### Adding Users to Groups Programmatically
```python
from django.contrib.auth.models import Group
from accounts.models import CustomUser

# Get user and group
user = CustomUser.objects.get(username='editor_user')
editors_group = Group.objects.get(name='Editors')

# Add user to group
user.groups.add(editors_group)
```

## Best Practices Implemented

1. **Separation of Concerns**: Permissions defined in models, enforced in views
2. **Defense in Depth**: Multiple layers of security (login, permissions, ownership)
3. **User Experience**: Clear feedback and appropriate UI based on permissions
4. **Maintainability**: Centralized permission management through groups
5. **Scalability**: Easy to add new permissions and groups as needed

## Troubleshooting

### Common Issues
1. **Permissions Not Working**: Ensure migrations are applied after adding permissions
2. **Users Can't Access**: Verify users are assigned to appropriate groups
3. **Templates Not Updating**: Check that permission checks use correct permission names

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

This implementation provides a robust, scalable permission system that can be easily extended for additional models and use cases.
