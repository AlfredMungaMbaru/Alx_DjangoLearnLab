# Django Security Best Practices Implementation

This document outlines the comprehensive security measures implemented in the BookShelf application.

## Table of Contents
1. [Security Settings](#security-settings)
2. [CSRF Protection](#csrf-protection)
3. [XSS Prevention](#xss-prevention)
4. [SQL Injection Prevention](#sql-injection-prevention)
5. [Content Security Policy](#content-security-policy)
6. [Secure Headers](#secure-headers)
7. [Authentication & Authorization](#authentication--authorization)
8. [Input Validation](#input-validation)
9. [Logging & Monitoring](#logging--monitoring)
10. [Testing Security Features](#testing-security-features)

## Security Settings

### Core Security Settings in `settings.py`:

```python
# Security Settings
DEBUG = False  # Always False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.yourdomain.com']

# Browser Security
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# HTTPS Settings (for production)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie Security
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Password Security
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

## CSRF Protection

### Implementation:
1. **CSRF Middleware**: Enabled in `MIDDLEWARE` settings
2. **Template Tags**: All forms include `{% csrf_token %}`
3. **View Decorators**: Critical views use `@csrf_protect`
4. **AJAX Requests**: Include CSRF token in headers

### Example Form:
```html
<form method="post">
    {% csrf_token %}
    <input type="text" name="title" required>
    <button type="submit">Submit</button>
</form>
```

### AJAX CSRF:
```javascript
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});
```

## XSS Prevention

### Template Security:
- **Auto-escaping**: Django templates auto-escape by default
- **Manual Escaping**: Use `{{ variable|escape }}` when needed
- **Safe Filter**: Only use `|safe` for trusted content

### Content Security Policy:
```python
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_CONNECT_SRC = ("'self'",)
```

### View-level XSS Protection:
```python
from django.utils.html import escape

def secure_view(request):
    user_input = escape(request.GET.get('query', ''))
    # Process escaped input
```

## SQL Injection Prevention

### ORM Usage:
- **Always use Django ORM**: Avoid raw SQL queries
- **Parameterized Queries**: When raw SQL is necessary, use parameters
- **Input Validation**: Validate all user inputs

### Safe Query Examples:
```python
# Safe - Using ORM
books = Book.objects.filter(title__icontains=search_term)

# Safe - Parameterized raw SQL (if needed)
books = Book.objects.raw("SELECT * FROM books WHERE title LIKE %s", [f"%{search_term}%"])

# UNSAFE - Never do this
# books = Book.objects.raw(f"SELECT * FROM books WHERE title LIKE '%{search_term}%'")
```

## Content Security Policy

### CSP Configuration:
```python
# In settings.py
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")  # Minimize unsafe-inline
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "https:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)
```

### CSP Headers:
The CSP middleware automatically adds appropriate headers to responses.

## Secure Headers

### Security Headers Added:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Content-Security-Policy: [policy]`

### Implementation in Views:
```python
def secure_view(request):
    response = render(request, 'template.html')
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    return response
```

## Authentication & Authorization

### Custom User Model:
- Extended `AbstractUser` with additional fields
- Custom user manager for enhanced functionality

### Permission System:
- **Custom Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Groups**: Viewers, Editors, Admins with different permission levels
- **Decorators**: `@permission_required` on all sensitive views

### Permission Decorators:
```python
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    # View logic here
```

## Input Validation

### Form Validation:
```python
class BookForm(forms.ModelForm):
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if isbn and not re.match(r'^\d{10}(\d{3})?$', isbn):
            raise forms.ValidationError('Invalid ISBN format')
        return isbn
```

### View-level Validation:
```python
def search_view(request):
    query = request.GET.get('q', '').strip()
    
    if len(query) > 100:
        return JsonResponse({'error': 'Query too long'}, status=400)
    
    if not query:
        return JsonResponse({'error': 'Query required'}, status=400)
```

## Logging & Monitoring

### Security Logging:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'security': {
            'handlers': ['security'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Security Events Logged:
- Login attempts (successful/failed)
- Permission denials
- Invalid input attempts
- API access attempts
- Form submissions

## Testing Security Features

### Security Test Page:
Visit `/bookshelf/security-test/` to test:
- CSRF protection
- XSS prevention
- Security headers
- API endpoint security

### Manual Security Tests:

1. **CSRF Test**:
   - Try submitting forms without CSRF token
   - Should receive 403 Forbidden

2. **XSS Test**:
   - Enter `<script>alert('XSS')</script>` in form fields
   - Should be escaped and not executed

3. **SQL Injection Test**:
   - Enter `'; DROP TABLE books; --` in search fields
   - Should be safely handled by ORM

4. **Header Test**:
   - Check browser dev tools for security headers
   - Verify CSP, X-Frame-Options, etc.

### Automated Security Checks:
```bash
# Run Django security check
python manage.py check --deploy

# Check for common security issues
python -m bandit -r . -f json
```

## Production Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use HTTPS (SSL/TLS certificates)
- [ ] Set secure cookie flags
- [ ] Configure CSP headers
- [ ] Set up proper logging
- [ ] Regular security updates
- [ ] Monitor for vulnerabilities
- [ ] Backup database regularly
- [ ] Use environment variables for secrets

## Security Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [Django Security Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

**Note**: This implementation follows Django security best practices and provides defense against common web vulnerabilities including CSRF, XSS, SQL injection, and clickjacking attacks.
