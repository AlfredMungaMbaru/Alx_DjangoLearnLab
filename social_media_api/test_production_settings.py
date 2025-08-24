#!/usr/bin/env python3
"""
Test script to verify production settings configuration
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.insert(0, '/home/munga/Desktop/Alx/Alx_DjangoLearnLab/social_media_api')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')

# Setup Django
django.setup()

from django.conf import settings

def test_production_settings():
    """Test that production settings are properly configured"""
    
    print("🔍 Checking Django Settings for Production Configuration...")
    print("=" * 60)
    
    # Test DEBUG setting
    print(f"DEBUG setting: {settings.DEBUG}")
    if settings.DEBUG == False:
        print("✅ DEBUG is set to False (Production Ready)")
    else:
        print("❌ DEBUG is set to True (NOT Production Ready)")
    
    # Test ALLOWED_HOSTS
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS != ['*']:
        print("✅ ALLOWED_HOSTS is configured")
    else:
        print("⚠️  ALLOWED_HOSTS should be configured for production")
    
    # Test SECRET_KEY
    if settings.SECRET_KEY and not settings.SECRET_KEY.startswith('django-insecure'):
        print("✅ SECRET_KEY is configured (secure)")
    elif settings.SECRET_KEY.startswith('django-insecure'):
        print("⚠️  SECRET_KEY appears to be default/insecure")
    
    # Test Database Configuration
    db_engine = settings.DATABASES['default']['ENGINE']
    print(f"Database Engine: {db_engine}")
    if 'postgresql' in db_engine:
        print("✅ PostgreSQL configured for production")
    elif 'sqlite' in db_engine:
        print("⚠️  SQLite is configured (consider PostgreSQL for production)")
    
    # Test Security Settings (if DEBUG is False)
    if not settings.DEBUG:
        security_settings = [
            ('SECURE_BROWSER_XSS_FILTER', getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False)),
            ('SECURE_CONTENT_TYPE_NOSNIFF', getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False)),
            ('SECURE_HSTS_SECONDS', getattr(settings, 'SECURE_HSTS_SECONDS', 0)),
            ('SESSION_COOKIE_SECURE', getattr(settings, 'SESSION_COOKIE_SECURE', False)),
            ('CSRF_COOKIE_SECURE', getattr(settings, 'CSRF_COOKIE_SECURE', False)),
        ]
        
        print("\n🔒 Security Settings:")
        for setting_name, setting_value in security_settings:
            if setting_value:
                print(f"✅ {setting_name}: {setting_value}")
            else:
                print(f"❌ {setting_name}: {setting_value}")
    
    print("\n" + "=" * 60)
    
    # Overall assessment
    if not settings.DEBUG:
        print("🎉 Primary production requirement met: DEBUG = False")
        return True
    else:
        print("❌ CRITICAL: DEBUG is not False for production!")
        return False

if __name__ == "__main__":
    # Test with no environment variables (should default to production settings)
    print("Testing default settings (no environment variables)...")
    success = test_production_settings()
    
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Production settings check")
    
    # Show how to run with explicit environment variables
    print("\n" + "=" * 60)
    print("💡 To run in development mode, set environment variables:")
    print("export DEBUG=True")
    print("export DJANGO_ENV=development")
    print("\n💡 To run in production mode, set environment variables:")
    print("export DEBUG=False")
    print("export DJANGO_ENV=production")
    print("export SECRET_KEY=your-secure-secret-key")
    print("export ALLOWED_HOSTS=your-domain.com,www.your-domain.com")
