#!/usr/bin/env python3
"""
HTTPS Security Configuration Verification Script

This script verifies that all HTTPS and security settings are properly configured
in the Django application according to security best practices.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.test import RequestFactory
from django.http import HttpResponse

def check_https_settings():
    """Check HTTPS-related Django settings."""
    print("🔒 HTTPS Security Configuration Check")
    print("=" * 50)
    
    checks = {
        'HTTPS Enforcement': {
            'SECURE_SSL_REDIRECT': getattr(settings, 'SECURE_SSL_REDIRECT', False),
            'SECURE_PROXY_SSL_HEADER': getattr(settings, 'SECURE_PROXY_SSL_HEADER', None) is not None,
        },
        'HSTS Configuration': {
            'SECURE_HSTS_SECONDS': getattr(settings, 'SECURE_HSTS_SECONDS', 0) > 0,
            'SECURE_HSTS_INCLUDE_SUBDOMAINS': getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False),
            'SECURE_HSTS_PRELOAD': getattr(settings, 'SECURE_HSTS_PRELOAD', False),
        },
        'Secure Cookies': {
            'SESSION_COOKIE_SECURE': getattr(settings, 'SESSION_COOKIE_SECURE', False),
            'CSRF_COOKIE_SECURE': getattr(settings, 'CSRF_COOKIE_SECURE', False),
            'SESSION_COOKIE_HTTPONLY': getattr(settings, 'SESSION_COOKIE_HTTPONLY', False),
            'CSRF_COOKIE_HTTPONLY': getattr(settings, 'CSRF_COOKIE_HTTPONLY', False),
        },
        'Security Headers': {
            'X_FRAME_OPTIONS': getattr(settings, 'X_FRAME_OPTIONS', None) == 'DENY',
            'SECURE_CONTENT_TYPE_NOSNIFF': getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False),
            'SECURE_BROWSER_XSS_FILTER': getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False),
            'SECURE_REFERRER_POLICY': getattr(settings, 'SECURE_REFERRER_POLICY', None) is not None,
        },
        'Content Security Policy': {
            'CSP_DEFAULT_SRC': hasattr(settings, 'CSP_DEFAULT_SRC'),
            'CSP_SCRIPT_SRC': hasattr(settings, 'CSP_SCRIPT_SRC'),
            'CSP_STYLE_SRC': hasattr(settings, 'CSP_STYLE_SRC'),
        }
    }
    
    for category, tests in checks.items():
        print(f"\n📋 {category}:")
        for setting, is_configured in tests.items():
            status = "✅" if is_configured else "❌"
            value = getattr(settings, setting, 'Not set')
            print(f"  {status} {setting}: {value}")
    
    return checks

def check_production_readiness():
    """Check if settings are ready for production deployment."""
    print(f"\n🚀 Production Readiness Check:")
    print("-" * 30)
    
    production_checks = {
        'DEBUG disabled': not getattr(settings, 'DEBUG', True),
        'ALLOWED_HOSTS configured': len(getattr(settings, 'ALLOWED_HOSTS', [])) > 0,
        'SECRET_KEY secure': len(getattr(settings, 'SECRET_KEY', '')) > 30,
        'Database configured': 'sqlite3' not in settings.DATABASES['default']['ENGINE'] or settings.DEBUG,
    }
    
    for check, passed in production_checks.items():
        status = "✅" if passed else "⚠️"
        print(f"  {status} {check}")
    
    return production_checks

def test_security_middleware():
    """Test that security middleware is properly configured."""
    print(f"\n🛡️ Security Middleware Check:")
    print("-" * 30)
    
    required_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    middleware_checks = {}
    for middleware in required_middleware:
        is_present = middleware in settings.MIDDLEWARE
        middleware_checks[middleware] = is_present
        status = "✅" if is_present else "❌"
        print(f"  {status} {middleware.split('.')[-1]}")
    
    return middleware_checks

def run_django_security_check():
    """Run Django's built-in security check."""
    print(f"\n🔍 Django Security Check:")
    print("-" * 25)
    
    try:
        # Capture the output of the security check
        from io import StringIO
        from django.core.management.base import OutputWrapper
        
        out = StringIO()
        call_command('check', '--deploy', stdout=OutputWrapper(out))
        output = out.getvalue()
        
        if not output.strip() or "No issues found" in output:
            print("  ✅ No security issues found!")
            return True
        else:
            print("  ⚠️ Security issues detected:")
            print(f"     {output}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error running security check: {e}")
        return False

def generate_security_summary():
    """Generate a summary of security configuration."""
    print(f"\n📊 Security Configuration Summary:")
    print("=" * 40)
    
    # Check various security aspects
    https_checks = check_https_settings()
    production_checks = check_production_readiness()
    middleware_checks = test_security_middleware()
    django_check = run_django_security_check()
    
    # Calculate overall security score
    total_checks = 0
    passed_checks = 0
    
    for category in https_checks.values():
        for passed in category.values():
            total_checks += 1
            if passed:
                passed_checks += 1
    
    for passed in production_checks.values():
        total_checks += 1
        if passed:
            passed_checks += 1
    
    for passed in middleware_checks.values():
        total_checks += 1
        if passed:
            passed_checks += 1
    
    if django_check:
        passed_checks += 1
    total_checks += 1
    
    security_score = (passed_checks / total_checks) * 100
    
    print(f"\n🎯 Overall Security Score: {security_score:.1f}% ({passed_checks}/{total_checks})")
    
    if security_score >= 90:
        print("🟢 EXCELLENT: Your application has strong security configuration!")
    elif security_score >= 75:
        print("🟡 GOOD: Your application has good security, but there's room for improvement.")
    elif security_score >= 50:
        print("🟠 MODERATE: Your application needs security improvements.")
    else:
        print("🔴 POOR: Your application has significant security vulnerabilities.")
    
    return security_score

def show_next_steps():
    """Show recommended next steps for deployment."""
    print(f"\n📝 Next Steps for HTTPS Deployment:")
    print("-" * 35)
    print("1. 🔐 Obtain SSL/TLS certificate (Let's Encrypt recommended)")
    print("2. 🌐 Configure web server (Nginx/Apache) with HTTPS")
    print("3. 🔄 Set up automatic certificate renewal")
    print("4. 🧪 Test HTTPS configuration with SSL Labs")
    print("5. 📊 Monitor certificate expiration and security headers")
    print("6. 🔍 Regular security audits and updates")
    
    print(f"\n📚 Documentation References:")
    print("   • HTTPS_DEPLOYMENT_GUIDE.md - Web server configuration")
    print("   • SECURITY_REVIEW.md - Comprehensive security analysis")
    print("   • SECURITY_GUIDE.md - Detailed security implementation")

def main():
    """Main function to run all security checks."""
    print("🔐 Django HTTPS Security Verification")
    print("=" * 50)
    print("Verifying HTTPS and security configuration...")
    
    try:
        score = generate_security_summary()
        show_next_steps()
        
        print(f"\n✨ Security verification completed!")
        print(f"📄 See SECURITY_REVIEW.md for detailed analysis")
        
        return 0 if score >= 75 else 1
        
    except Exception as e:
        print(f"\n❌ Error during security verification: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
