# Social Media API - Deployment Guide

## 🚀 Production Deployment Guide

This guide covers deploying the Social Media API to various production environments including Heroku, AWS, DigitalOcean, and Docker-based deployments.

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Redis 6+ (for caching)
- Git
- Domain name (for HTTPS)

## 🔧 Environment Setup

### 1. Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Configure the following variables:

- `SECRET_KEY`: Django secret key (generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your domain names
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string

### 2. Dependencies

Install production dependencies:

```bash
pip install -r requirements.txt
```

## 🌊 Heroku Deployment

### Quick Deployment

Run the automated deployment script:

```bash
./deploy_heroku.sh
```

### Manual Deployment

1. **Install Heroku CLI**
   ```bash
   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh
   
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:essential-0
   ```

5. **Add Redis**
   ```bash
   heroku addons:create heroku-redis:mini
   ```

6. **Set Environment Variables**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set SECURE_SSL_REDIRECT=True
   heroku config:set SESSION_COOKIE_SECURE=True
   heroku config:set CSRF_COOKIE_SECURE=True
   ```

7. **Deploy**
   ```bash
   git push heroku main
   ```

8. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   ```

9. **Create Superuser**
   ```bash
   heroku run python manage.py createsuperuser
   ```

## 🐳 Docker Deployment

### Development Environment

```bash
docker-compose up --build
```

### Production Environment

1. **Build Image**
   ```bash
   docker build -t social-media-api .
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## ☁️ AWS Deployment

### Using Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**
   ```bash
   eb init
   ```

3. **Create Environment**
   ```bash
   eb create production
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

### Using EC2

1. **Launch EC2 Instance** (Ubuntu 20.04 LTS)

2. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx redis-server
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/AlfredMungaMbaru/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/social_media_api
   ```

5. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure PostgreSQL**
   ```bash
   sudo -u postgres createdb social_media_api
   sudo -u postgres createuser --interactive
   ```

7. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

8. **Run Migrations**
   ```bash
   python manage.py migrate --settings=social_media_api.settings_production
   ```

9. **Collect Static Files**
   ```bash
   python manage.py collectstatic --settings=social_media_api.settings_production
   ```

10. **Configure Gunicorn**
    ```bash
    # Create systemd service file
    sudo nano /etc/systemd/system/social-media-api.service
    ```

11. **Configure Nginx**
    ```bash
    sudo cp nginx.conf /etc/nginx/sites-available/social-media-api
    sudo ln -s /etc/nginx/sites-available/social-media-api /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    ```

## 🔒 Security Configuration

### SSL/HTTPS Setup

1. **Install Certbot** (for Let's Encrypt)
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain SSL Certificate**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

### Security Headers

The production settings include security headers:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security`

## 📊 Monitoring and Logging

### Application Monitoring

1. **Sentry Setup** (Error Tracking)
   ```bash
   pip install sentry-sdk
   ```

   Add to settings:
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration
   
   sentry_sdk.init(
       dsn="YOUR_SENTRY_DSN",
       integrations=[DjangoIntegration()],
       traces_sample_rate=1.0,
   )
   ```

2. **Log Files**
   - Application logs: `/app/django.log`
   - Nginx logs: `/var/log/nginx/`
   - System logs: `/var/log/syslog`

### Health Checks

Create a health check endpoint:

```python
# Add to urls.py
path('health/', views.health_check, name='health-check'),

# Add to views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "healthy"})
    except Exception as e:
        return JsonResponse({"status": "unhealthy", "error": str(e)}, status=500)
```

## 🔄 Database Management

### Backups

```bash
# PostgreSQL backup
pg_dump social_media_api > backup.sql

# Restore
psql social_media_api < backup.sql
```

### Migrations

```bash
# Run migrations
python manage.py migrate --settings=social_media_api.settings_production

# Create migrations
python manage.py makemigrations --settings=social_media_api.settings_production
```

## 📈 Performance Optimization

### Database Optimization

1. **Database Indexing**
   - Add indexes to frequently queried fields
   - Use `select_related()` and `prefetch_related()`

2. **Connection Pooling**
   ```python
   # Add to settings
   DATABASES['default']['CONN_MAX_AGE'] = 60
   ```

### Caching

Redis caching is configured for:
- Session storage
- Query caching
- Template caching

### Static Files

- Use CDN for static files in production
- Enable compression with WhiteNoise
- Set appropriate cache headers

## 🔧 Maintenance

### Regular Tasks

1. **Update Dependencies**
   ```bash
   pip list --outdated
   pip install -U package-name
   ```

2. **Database Maintenance**
   ```bash
   # PostgreSQL vacuum
   sudo -u postgres psql -c "VACUUM ANALYZE;"
   ```

3. **Log Rotation**
   ```bash
   # Configure logrotate
   sudo nano /etc/logrotate.d/social-media-api
   ```

### Troubleshooting

1. **Check Logs**
   ```bash
   # Application logs
   tail -f django.log
   
   # Heroku logs
   heroku logs --tail
   
   # Docker logs
   docker logs container-name
   ```

2. **Database Issues**
   ```bash
   # Check database connectivity
   python manage.py dbshell
   
   # Reset migrations (if needed)
   python manage.py migrate --fake-initial
   ```

3. **Static Files Issues**
   ```bash
   # Recollect static files
   python manage.py collectstatic --clear --noinput
   ```

## 📱 API Documentation

The API is accessible at:
- Development: `http://localhost:8000/api/`
- Production: `https://your-domain.com/api/`

### Endpoints

- `/api/accounts/` - User management
- `/api/posts/` - Posts and comments
- `/api/notifications/` - Notifications
- `/admin/` - Django admin interface

## 🛠️ Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| Debug | True | False |
| Database | SQLite | PostgreSQL |
| Static Files | Django dev server | WhiteNoise/CDN |
| Security | Basic | Full headers |
| Caching | None | Redis |
| HTTPS | Optional | Required |

## 📞 Support

For deployment issues:
1. Check the logs first
2. Verify environment variables
3. Ensure all dependencies are installed
4. Check database connectivity
5. Verify static files are collected

## 🔗 Useful Links

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Heroku Django Documentation](https://devcenter.heroku.com/articles/django-app-configuration)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Nginx Configuration](https://nginx.org/en/docs/)
