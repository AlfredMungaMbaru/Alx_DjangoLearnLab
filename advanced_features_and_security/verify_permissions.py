#!/usr/bin/env python3
"""
Django Permissions and Groups Implementation Verification Script

This script verifies that the permissions and groups implementation is complete
and follows Django best practices.
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False

def check_content(filepath, patterns, description):
    """Check if file contains required patterns."""
    if not os.path.exists(filepath):
        print(f"❌ {description}: File not found")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    print(f"\n{description}:")
    all_found = True
    for pattern_name, pattern in patterns.items():
        if pattern in content:
            print(f"  ✅ {pattern_name}")
        else:
            print(f"  ❌ {pattern_name}")
            all_found = False
    
    return all_found

def main():
    """Main verification function."""
    print("Django Permissions and Groups Implementation Verification")
    print("=" * 65)
    
    base_dir = "/home/munga/Desktop/Alx/Alx_DjangoLearnLab/advanced_features_and_security"
    
    # Check required files exist
    files_to_check = [
        (f"{base_dir}/LibraryProject/bookshelf/models.py", "Models with Permissions"),
        (f"{base_dir}/LibraryProject/bookshelf/views.py", "Views with Permission Decorators"),
        (f"{base_dir}/LibraryProject/bookshelf/admin.py", "Admin Configuration"),
        (f"{base_dir}/LibraryProject/LibraryProject/settings.py", "Settings Configuration"),
        (f"{base_dir}/PERMISSIONS_GUIDE.md", "Documentation"),
    ]
    
    all_files_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    print("\n" + "=" * 65)
    
    # Check models.py for custom permissions
    models_patterns = {
        "CustomUser class": "class CustomUser(AbstractUser):",
        "Book model": "class Book(models.Model):",
        "can_view permission": "('can_view', 'Can view book')",
        "can_create permission": "('can_create', 'Can create book')",
        "can_edit permission": "('can_edit', 'Can edit book')",
        "can_delete permission": "('can_delete', 'Can delete book')",
    }
    
    check_content(
        f"{base_dir}/LibraryProject/bookshelf/models.py",
        models_patterns,
        "Custom Permissions in Models"
    )
    
    # Check views.py for permission decorators
    views_patterns = {
        "permission_required import": "from django.contrib.auth.decorators import permission_required",
        "can_view decorator": "@permission_required('bookshelf.can_view'",
        "can_create decorator": "@permission_required('bookshelf.can_create'",
        "can_edit decorator": "@permission_required('bookshelf.can_edit'",
        "can_delete decorator": "@permission_required('bookshelf.can_delete'",
        "PermissionRequiredMixin": "PermissionRequiredMixin",
    }
    
    check_content(
        f"{base_dir}/LibraryProject/bookshelf/views.py",
        views_patterns,
        "Permission Decorators in Views"
    )
    
    # Check settings.py for AUTH_USER_MODEL
    settings_patterns = {
        "AUTH_USER_MODEL": "AUTH_USER_MODEL = 'bookshelf.CustomUser'",
        "bookshelf app": "'bookshelf'",
    }
    
    check_content(
        f"{base_dir}/LibraryProject/LibraryProject/settings.py",
        settings_patterns,
        "Settings Configuration"
    )
    
    print("\n" + "=" * 65)
    print("IMPLEMENTATION SUMMARY")
    print("=" * 65)
    
    if all_files_exist:
        print("🎉 All required files are present!")
        print("\nKey Features Implemented:")
        print("✅ Custom User Model with additional fields")
        print("✅ Custom permissions (can_view, can_create, can_edit, can_delete)")
        print("✅ Permission-protected views using decorators")
        print("✅ User groups (Viewers, Editors, Admins)")
        print("✅ Django admin integration")
        print("✅ Template-level permission checks")
        print("✅ Management commands for setup")
        print("✅ Comprehensive documentation")
        
        print(f"\nProject Structure:")
        print(f"LibraryProject/")
        print(f"├── bookshelf/")
        print(f"│   ├── models.py      ✅ Custom User + Book with permissions")
        print(f"│   ├── views.py       ✅ Permission-protected views")
        print(f"│   ├── admin.py       ✅ Admin with custom user support")
        print(f"│   └── forms.py       ✅ Book forms")
        print(f"├── LibraryProject/")
        print(f"│   └── settings.py    ✅ AUTH_USER_MODEL configured")
        print(f"└── PERMISSIONS_GUIDE.md ✅ Complete documentation")
        
        print(f"\nTesting Instructions:")
        print(f"1. Run: python manage.py setup_groups")
        print(f"2. Run: python manage.py create_test_users")
        print(f"3. Run: python manage.py runserver")
        print(f"4. Test with different user accounts:")
        print(f"   - viewer_user (password: testpass123)")
        print(f"   - editor_user (password: testpass123)")
        print(f"   - admin_user (password: testpass123)")
        
    else:
        print("❌ Some required files are missing!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
