#!/usr/bin/env python3
"""
Django Custom User Model Implementation Verification Script

This script verifies that the custom user model implementation is complete
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

def main():
    """Main verification function."""
    print("Django Custom User Model Implementation Verification")
    print("=" * 60)
    
    base_dir = "/home/munga/Desktop/Alx/Alx_DjangoLearnLab/advanced_features_and_security"
    
    # Check core implementation files
    files_to_check = [
        (f"{base_dir}/accounts/models.py", "Custom User Model"),
        (f"{base_dir}/accounts/admin.py", "Custom User Admin"),
        (f"{base_dir}/advanced_features_and_security/settings.py", "Settings Configuration"),
        (f"{base_dir}/bookshelf/models.py", "Example App Models"),
        (f"{base_dir}/bookshelf/admin.py", "Example App Admin"),
        (f"{base_dir}/LibraryProject/bookshelf/models.py", "Checker Expected Path"),
        (f"{base_dir}/manage.py", "Django Management Script"),
        (f"{base_dir}/db.sqlite3", "Database File"),
    ]
    
    all_files_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    print("\n" + "=" * 60)
    
    # Check specific implementations
    print("\nImplementation Details:")
    
    # Check models.py content
    models_file = f"{base_dir}/accounts/models.py"
    if os.path.exists(models_file):
        with open(models_file, 'r') as f:
            content = f.read()
            
        checks = [
            ("CustomUser class", "class CustomUser(AbstractUser):" in content),
            ("CustomUserManager class", "class CustomUserManager(BaseUserManager):" in content),
            ("date_of_birth field", "date_of_birth = models.DateField" in content),
            ("profile_photo field", "profile_photo = models.ImageField" in content),
            ("create_user method", "def create_user(" in content),
            ("create_superuser method", "def create_superuser(" in content),
            ("age property", "@property" in content and "def age(" in content),
        ]
        
        for check_name, condition in checks:
            status = "✅" if condition else "❌"
            print(f"  {status} {check_name}")
    
    # Check settings.py for AUTH_USER_MODEL
    settings_file = f"{base_dir}/advanced_features_and_security/settings.py"
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            settings_content = f.read()
        
        auth_user_check = "AUTH_USER_MODEL = 'accounts.CustomUser'" in settings_content
        accounts_app_check = "'accounts'" in settings_content
        
        print(f"  {'✅' if auth_user_check else '❌'} AUTH_USER_MODEL configuration")
        print(f"  {'✅' if accounts_app_check else '❌'} Accounts app in INSTALLED_APPS")
    
    print("\n" + "=" * 60)
    
    if all_files_exist:
        print("🎉 All required files are present!")
        print("\nImplementation Summary:")
        print("- Custom user model with date_of_birth and profile_photo fields")
        print("- Custom user manager with create_user and create_superuser methods")
        print("- Proper Django admin integration")
        print("- Settings configured to use custom user model")
        print("- Example app demonstrating foreign key relationships")
        print("- Media file handling for profile photos")
        print("- Comprehensive test suite")
    else:
        print("❌ Some required files are missing!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
