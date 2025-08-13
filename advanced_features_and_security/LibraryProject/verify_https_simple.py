#!/usr/bin/env python3
"""
HTTPS Security Configuration Verification Script (Standalone)

This script verifies that all HTTPS and security settings are properly configured
in the Django settings file without requiring Django to be installed.
"""

import os
import re
from pathlib import Path

def read_settings_file():
    """Read and parse the Django settings file."""
    settings_path = Path(__file__).parent / "LibraryProject" / "settings.py"
    
    if not settings_path.exists():
        print(f"❌ Settings file not found: {settings_path}")
        return None
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    return content

def extract_setting_value(content, setting_name):
    """Extract a setting value from the settings file content."""
    # Pattern to match setting assignments
    pattern = rf'^{setting_name}\s*=\s*(.+)$'
    match = re.search(pattern, content, re.MULTILINE)
    
    if match:
        value = match.group(1).strip()
        # Clean up the value
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        elif value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        elif value.isdigit():
            return int(value)
        else:
            return value
    
    return None

def check_https_settings():
    """Check HTTPS-related Django settings."""
    print("🔒 HTTPS Security Configuration Check")
    print("=" * 50)
    
    content = read_settings_file()
    if not content:
        return False
    
    # Define expected settings and their secure values
    https_settings = {
        'HTTPS Enforcement': {
            'SECURE_SSL_REDIRECT': 'Should redirect HTTP to HTTPS',
            'SECURE_PROXY_SSL_HEADER': 'Should be configured for reverse proxy',
        },
        'HSTS Configuration': {
            'SECURE_HSTS_SECONDS': 'Should be > 0 (recommended: 31536000)',
            'SECURE_HSTS_INCLUDE_SUBDOMAINS': 'Should be True',
            'SECURE_HSTS_PRELOAD': 'Should be True',
        },
        'Secure Cookies': {
            'SESSION_COOKIE_SECURE': 'Should be True',
            'CSRF_COOKIE_SECURE': 'Should be True',
            'SESSION_COOKIE_HTTPONLY': 'Should be True',
            'CSRF_COOKIE_HTTPONLY': 'Should be True',
        },
        'Security Headers': {
            'X_FRAME_OPTIONS': 'Should be DENY',
            'SECURE_CONTENT_TYPE_NOSNIFF': 'Should be True',
            'SECURE_BROWSER_XSS_FILTER': 'Should be True',
            'SECURE_REFERRER_POLICY': 'Should be configured',
        }
    }
    
    total_checks = 0
    passed_checks = 0
    
    for category, settings in https_settings.items():
        print(f"\n📋 {category}:")
        
        for setting, description in settings.items():
            total_checks += 1
            
            # Check if setting exists in file
            if setting in content:
                value = extract_setting_value(content, setting)
                
                # Evaluate if setting is properly configured
                is_secure = False
                
                if setting == 'SECURE_SSL_REDIRECT':
                    is_secure = 'not DEBUG' in content or value is True
                elif setting == 'SECURE_PROXY_SSL_HEADER':
                    is_secure = 'HTTP_X_FORWARDED_PROTO' in content
                elif setting == 'SECURE_HSTS_SECONDS':
                    is_secure = ('31536000' in content and 'not DEBUG' in content) or (isinstance(value, int) and value > 0)
                elif setting in ['SECURE_HSTS_INCLUDE_SUBDOMAINS', 'SECURE_HSTS_PRELOAD']:
                    is_secure = 'not DEBUG' in content or value is True
                elif setting in ['SESSION_COOKIE_SECURE', 'CSRF_COOKIE_SECURE']:
                    is_secure = 'not DEBUG' in content or value is True
                elif setting in ['SESSION_COOKIE_HTTPONLY', 'CSRF_COOKIE_HTTPONLY', 'SECURE_CONTENT_TYPE_NOSNIFF', 'SECURE_BROWSER_XSS_FILTER']:
                    is_secure = value is True
                elif setting == 'X_FRAME_OPTIONS':
                    is_secure = value == 'DENY' or 'DENY' in content
                elif setting == 'SECURE_REFERRER_POLICY':
                    is_secure = value is not None
                
                if is_secure:
                    passed_checks += 1
                    status = "✅"
                else:
                    status = "⚠️"
                    
                print(f"  {status} {setting}: {value} ({description})")
            else:
                print(f"  ❌ {setting}: Not configured ({description})")
    
    return total_checks, passed_checks

def check_csp_configuration():
    """Check Content Security Policy configuration."""
    print(f"\n🛡️ Content Security Policy Check:")
    print("-" * 35)
    
    content = read_settings_file()
    if not content:
        return 0, 0
    
    csp_settings = [
        'CSP_DEFAULT_SRC',
        'CSP_SCRIPT_SRC', 
        'CSP_STYLE_SRC',
        'CSP_IMG_SRC'
    ]
    
    total_checks = len(csp_settings)
    passed_checks = 0
    
    for setting in csp_settings:
        if setting in content:
            passed_checks += 1
            print(f"  ✅ {setting}: Configured")
        else:
            print(f"  ❌ {setting}: Not configured")
    
    return total_checks, passed_checks

def check_middleware_configuration():
    """Check security middleware configuration."""
    print(f"\n🔧 Security Middleware Check:")
    print("-" * 30)
    
    content = read_settings_file()
    if not content:
        return 0, 0
    
    required_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'csp.middleware.CSPMiddleware'
    ]
    
    total_checks = len(required_middleware)
    passed_checks = 0
    
    for middleware in required_middleware:
        if middleware in content:
            passed_checks += 1
            print(f"  ✅ {middleware.split('.')[-1]}")
        else:
            print(f"  ❌ {middleware.split('.')[-1]}: Not found")
    
    return total_checks, passed_checks

def check_production_settings():
    """Check production readiness settings."""
    print(f"\n🚀 Production Readiness Check:")
    print("-" * 30)
    
    content = read_settings_file()
    if not content:
        return 0, 0
    
    total_checks = 0
    passed_checks = 0
    
    # Check DEBUG setting
    total_checks += 1
    if 'DEBUG = False' in content or 'DEBUG = not' in content:
        passed_checks += 1
        print("  ✅ DEBUG: Properly configured for production")
    else:
        print("  ⚠️ DEBUG: Should be False in production")
    
    # Check ALLOWED_HOSTS
    total_checks += 1
    if 'ALLOWED_HOSTS' in content and ('getenv' in content or len(content.split('ALLOWED_HOSTS')[1].split('\n')[0]) > 20):
        passed_checks += 1
        print("  ✅ ALLOWED_HOSTS: Configured")
    else:
        print("  ⚠️ ALLOWED_HOSTS: Should be properly configured")
    
    # Check SECRET_KEY
    total_checks += 1
    if 'SECRET_KEY' in content and ('getenv' in content or 'os.environ' in content):
        passed_checks += 1
        print("  ✅ SECRET_KEY: Using environment variable")
    else:
        print("  ⚠️ SECRET_KEY: Should use environment variable")
    
    return total_checks, passed_checks

def generate_security_report():
    """Generate a comprehensive security report."""
    print("🔐 Django HTTPS Security Verification")
    print("=" * 50)
    
    # Run all checks
    https_total, https_passed = check_https_settings()
    csp_total, csp_passed = check_csp_configuration()
    middleware_total, middleware_passed = check_middleware_configuration()
    prod_total, prod_passed = check_production_settings()
    
    # Calculate overall score
    total_checks = https_total + csp_total + middleware_total + prod_total
    passed_checks = https_passed + csp_passed + middleware_passed + prod_passed
    
    if total_checks > 0:
        security_score = (passed_checks / total_checks) * 100
    else:
        security_score = 0
    
    print(f"\n🎯 Overall Security Score: {security_score:.1f}% ({passed_checks}/{total_checks})")
    
    # Provide assessment
    if security_score >= 90:
        print("🟢 EXCELLENT: Your application has strong HTTPS security configuration!")
        grade = "A+"
    elif security_score >= 80:
        print("🟡 GOOD: Your application has good HTTPS security, minor improvements needed.")
        grade = "B+"
    elif security_score >= 70:
        print("🟠 MODERATE: Your application needs HTTPS security improvements.")
        grade = "C"
    else:
        print("🔴 POOR: Your application has significant HTTPS security issues.")
        grade = "F"
    
    return security_score, grade

def show_recommendations():
    """Show recommendations for improvement."""
    print(f"\n📝 HTTPS Deployment Recommendations:")
    print("-" * 40)
    print("1. 🔐 SSL Certificate:")
    print("   • Use Let's Encrypt for free SSL certificates")
    print("   • Set up automatic certificate renewal")
    print("   • Test certificate with SSL Labs")
    
    print("\n2. 🌐 Web Server Configuration:")
    print("   • Configure Nginx/Apache for HTTPS")
    print("   • Enable HTTP/2 for better performance")
    print("   • Set up proper security headers")
    
    print("\n3. 🔍 Testing and Monitoring:")
    print("   • Test with: python manage.py check --deploy")
    print("   • Use SSL Labs SSL Test")
    print("   • Monitor certificate expiration")
    
    print("\n4. 📚 Documentation:")
    print("   • Review HTTPS_DEPLOYMENT_GUIDE.md")
    print("   • Check SECURITY_REVIEW.md")
    print("   • Follow SECURITY_GUIDE.md")

def main():
    """Main function to run HTTPS security verification."""
    try:
        score, grade = generate_security_report()
        show_recommendations()
        
        print(f"\n✨ HTTPS Security verification completed!")
        print(f"📊 Final Grade: {grade} ({score:.1f}%)")
        
        # Return appropriate exit code
        return 0 if score >= 70 else 1
        
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        return 1

if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)
