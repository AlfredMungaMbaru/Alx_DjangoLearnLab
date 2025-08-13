# HTTPS Deployment Configuration Guide

This document provides comprehensive instructions for configuring your web server to support HTTPS and SSL/TLS certificates for the Django BookShelf application.

## Table of Contents
1. [SSL/TLS Certificate Setup](#ssltls-certificate-setup)
2. [Nginx Configuration](#nginx-configuration)
3. [Apache Configuration](#apache-configuration)
4. [Django Settings Verification](#django-settings-verification)
5. [Security Testing](#security-testing)
6. [Troubleshooting](#troubleshooting)

## SSL/TLS Certificate Setup

### Option 1: Let's Encrypt (Free SSL Certificate)

Let's Encrypt provides free SSL certificates. Install Certbot:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

Obtain SSL certificate:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Option 2: Commercial SSL Certificate

1. Purchase SSL certificate from a trusted CA
2. Generate Certificate Signing Request (CSR)
3. Install the certificate files on your server

### Option 3: Self-Signed Certificate (Development Only)

**Warning: Only use for development/testing**

```bash
# Generate private key
openssl genrsa -out server.key 2048

# Generate certificate signing request
openssl req -new -key server.key -out server.csr

# Generate self-signed certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

## Nginx Configuration

### Complete Nginx Configuration for HTTPS

Create or update `/etc/nginx/sites-available/bookshelf`:

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect all HTTP requests to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS server configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    # SSL Configuration for Security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS Header (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:;" always;
    
    # Django Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        
        # Enable HTTP/2 Server Push (optional)
        http2_push_preload on;
    }
    
    # Static files
    location /static/ {
        alias /path/to/your/django/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /path/to/your/django/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # Security.txt (optional but recommended)
    location = /.well-known/security.txt {
        alias /path/to/security.txt;
    }
}
```

### Enable the configuration:

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/bookshelf /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## Apache Configuration

### Apache HTTPS Configuration

Create or update your Apache virtual host configuration:

```apache
# HTTP to HTTPS redirect
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # Redirect all HTTP to HTTPS
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS Virtual Host
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key
    SSLCertificateChainFile /path/to/your/chain.crt
    
    # SSL Security Configuration
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256
    SSLHonorCipherOrder on
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # Django Application (using mod_wsgi)
    WSGIDaemonProcess bookshelf python-path=/path/to/your/django/project
    WSGIProcessGroup bookshelf
    WSGIScriptAlias / /path/to/your/django/project/wsgi.py
    
    # Static files
    Alias /static/ /path/to/your/django/staticfiles/
    <Directory /path/to/your/django/staticfiles/>
        Require all granted
    </Directory>
    
    # Media files
    Alias /media/ /path/to/your/django/media/
    <Directory /path/to/your/django/media/>
        Require all granted
    </Directory>
    
    # Django project directory
    <Directory /path/to/your/django/project/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

### Enable required Apache modules:

```bash
sudo a2enmod ssl
sudo a2enmod headers
sudo a2enmod rewrite
sudo systemctl restart apache2
```

## Django Settings Verification

Ensure your Django settings are properly configured for production:

### Environment Variables

Create a `.env` file for production settings:

```bash
# .env file for production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=your-database-url-here
```

### Production Settings Check

Run Django's deployment check:

```bash
python manage.py check --deploy
```

This will verify all security settings are properly configured.

## Security Testing

### 1. SSL/TLS Configuration Test

Test your SSL configuration:

```bash
# Test SSL certificate
openssl s_client -connect yourdomain.com:443

# Check certificate details
openssl x509 -in certificate.crt -text -noout
```

### 2. Online Security Tests

Use these online tools to verify your HTTPS configuration:

- **SSL Labs SSL Test**: https://www.ssllabs.com/ssltest/
- **Mozilla Observatory**: https://observatory.mozilla.org/
- **Security Headers**: https://securityheaders.com/

### 3. Test HTTPS Redirects

```bash
# Test HTTP to HTTPS redirect
curl -I http://yourdomain.com

# Should return 301 redirect to HTTPS
```

### 4. Test Security Headers

```bash
# Check security headers
curl -I https://yourdomain.com

# Look for:
# Strict-Transport-Security
# X-Frame-Options
# X-Content-Type-Options
# X-XSS-Protection
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Mixed Content Warnings

**Problem**: HTTPS page loading HTTP resources
**Solution**: Update all URLs to use HTTPS or protocol-relative URLs

#### 2. Certificate Chain Issues

**Problem**: Browser shows certificate warnings
**Solution**: Ensure complete certificate chain is installed

```bash
# Check certificate chain
openssl s_client -connect yourdomain.com:443 -showcerts
```

#### 3. HSTS Not Working

**Problem**: HSTS header not being sent
**Solution**: Verify web server configuration and Django settings

#### 4. Performance Issues

**Problem**: Slow HTTPS connections
**Solution**: 
- Enable HTTP/2
- Use session resumption
- Optimize cipher suites

### Debug Commands

```bash
# Check nginx configuration
sudo nginx -t

# Check Apache configuration
sudo apache2ctl configtest

# Check SSL certificate expiration
openssl x509 -enddate -noout -in certificate.crt

# Monitor SSL traffic
sudo tcpdump -i any port 443

# Check Django logs
tail -f /path/to/django/logs/django.log
```

## Automation Scripts

### Certificate Renewal Script

Create a cron job for automatic certificate renewal:

```bash
# /etc/cron.d/certbot-renewal
0 12 * * * /usr/bin/certbot renew --quiet --deploy-hook "systemctl reload nginx"
```

### Deployment Script

```bash
#!/bin/bash
# deploy.sh - HTTPS deployment script

set -e

echo "Starting HTTPS deployment..."

# Update Django settings
export DEBUG=False
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"

# Collect static files
python manage.py collectstatic --noinput

# Run security checks
python manage.py check --deploy

# Restart services
sudo systemctl restart nginx
sudo systemctl restart gunicorn

echo "HTTPS deployment completed successfully!"
```

## Security Checklist

- [ ] SSL/TLS certificate installed and valid
- [ ] HTTP to HTTPS redirects working
- [ ] HSTS headers configured
- [ ] Security headers present
- [ ] Django SECURE_SSL_REDIRECT enabled
- [ ] Secure cookies configured
- [ ] Certificate auto-renewal setup
- [ ] Security tests passing
- [ ] Performance optimized
- [ ] Monitoring configured

---

**Note**: Always test these configurations in a staging environment before applying to production. Keep certificates and private keys secure and regularly updated.
