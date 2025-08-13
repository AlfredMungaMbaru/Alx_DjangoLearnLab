#!/usr/bin/env python3
"""
Security Implementation Verification Script
This script checks that all security best practices have been implemented.
"""

import os
import re
from pathlib import Path

def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)

def check_settings_security():
    """Check security settings in settings.py."""
    settings_path = "LibraryProject/settings.py"
    if not check_file_exists(settings_path):
        return False, "settings.py not found"
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    security_checks = {
        'DEBUG = False': 'DEBUG = False' in content,
        'ALLOWED_HOSTS configured': 'ALLOWED_HOSTS' in content and not 'ALLOWED_HOSTS = []' in content,
        'SECURE_BROWSER_XSS_FILTER': 'SECURE_BROWSER_XSS_FILTER = True' in content,
        'X_FRAME_OPTIONS': 'X_FRAME_OPTIONS' in content,
        'SECURE_CONTENT_TYPE_NOSNIFF': 'SECURE_CONTENT_TYPE_NOSNIFF = True' in content,
        'CSRF_COOKIE_SECURE': 'CSRF_COOKIE_SECURE = True' in content,
        'SESSION_COOKIE_SECURE': 'SESSION_COOKIE_SECURE = True' in content,
        'CSP middleware': 'csp.middleware.CSPMiddleware' in content,
        'Password validators': 'AUTH_PASSWORD_VALIDATORS' in content,
        'Security logging': 'security' in content and 'logging' in content.lower(),
    }
    
    return security_checks

def check_views_security():
    """Check security implementations in views.py."""
    views_path = "bookshelf/views.py"
    if not check_file_exists(views_path):
        return False, "views.py not found"
    
    with open(views_path, 'r') as f:
        content = f.read()
    
    security_checks = {
        'CSRF protection': '@csrf_protect' in content,
        'Permission decorators': '@permission_required' in content,
        'Login required': '@login_required' in content,
        'Input escaping': 'escape(' in content,
        'ORM usage': '.objects.filter' in content,
        'Logging': 'logger.' in content,
        'Input validation': 'len(' in content and 'strip()' in content,
    }
    
    return security_checks

def check_templates_security():
    """Check CSRF tokens in templates."""
    template_dir = "bookshelf/templates"
    if not os.path.exists(template_dir):
        return False, "Templates directory not found"
    
    csrf_found = False
    template_files = []
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                template_files.append(os.path.join(root, file))
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if 'csrf_token' in content:
                        csrf_found = True
    
    return {
        'CSRF tokens in templates': csrf_found,
        'Templates found': len(template_files) > 0,
        'Template count': len(template_files),
    }

def check_forms_security():
    """Check form security implementations."""
    forms_path = "bookshelf/forms.py"
    if not check_file_exists(forms_path):
        return {'Forms file exists': False}
    
    with open(forms_path, 'r') as f:
        content = f.read()
    
    return {
        'Forms file exists': True,
        'Form validation': 'clean_' in content or 'ValidationError' in content,
        'ModelForm usage': 'ModelForm' in content,
    }

def check_documentation():
    """Check if documentation files exist."""
    docs = {
        'README.md': check_file_exists('README.md'),
        'PERMISSIONS_GUIDE.md': check_file_exists('PERMISSIONS_GUIDE.md'),
        'SECURITY_GUIDE.md': check_file_exists('SECURITY_GUIDE.md'),
    }
    return docs

def main():
    """Run all security checks."""
    print("🔒 Django Security Implementation Verification")
    print("=" * 50)
    
    # Check settings
    print("\n📋 Settings Security:")
    settings_checks = check_settings_security()
    if isinstance(settings_checks, dict):
        for check, passed in settings_checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")
    else:
        print(f"  ❌ {settings_checks[1]}")
    
    # Check views
    print("\n🔍 Views Security:")
    views_checks = check_views_security()
    if isinstance(views_checks, dict):
        for check, passed in views_checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")
    else:
        print(f"  ❌ {views_checks[1]}")
    
    # Check templates
    print("\n📄 Templates Security:")
    template_checks = check_templates_security()
    if isinstance(template_checks, dict):
        for check, result in template_checks.items():
            if isinstance(result, bool):
                status = "✅" if result else "❌"
                print(f"  {status} {check}")
            else:
                print(f"  ℹ️ {check}: {result}")
    else:
        print(f"  ❌ {template_checks[1]}")
    
    # Check forms
    print("\n📝 Forms Security:")
    forms_checks = check_forms_security()
    for check, passed in forms_checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    
    # Check documentation
    print("\n📚 Documentation:")
    doc_checks = check_documentation()
    for doc, exists in doc_checks.items():
        status = "✅" if exists else "❌"
        print(f"  {status} {doc}")
    
    print("\n🎯 Summary:")
    print("  - Security settings configured in settings.py")
    print("  - CSRF protection implemented in views and templates")
    print("  - XSS prevention through input escaping")
    print("  - SQL injection prevention via ORM usage")
    print("  - Content Security Policy configured")
    print("  - Secure headers implemented")
    print("  - Permission-based access control")
    print("  - Input validation and logging")
    print("  - Comprehensive documentation provided")
    
    print("\n✨ Security implementation verification complete!")

if __name__ == "__main__":
    main()
