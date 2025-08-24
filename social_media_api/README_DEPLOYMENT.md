# Social Media API - Production Deployment

## 🚀 Quick Start

### Option 1: Heroku Deployment (Recommended for beginners)

```bash
# Run the automated deployment script
./deploy_heroku.sh
```

### Option 2: Docker Deployment

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up -d
```

### Option 3: Manual VPS Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🔧 Environment Configuration

Copy the environment template:
```bash
cp .env.example .env
```

Configure the following variables:
- `SECRET_KEY`: Generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your domain names
- `DATABASE_URL`: PostgreSQL connection string

## 📊 Testing the Deployment

Test your deployed application:
```bash
python test_deployment.py https://your-app-url.com
```

## 🔗 Live Application

Once deployed, your API will be available at:
- **API Base URL**: `https://your-domain.com/api/`
- **Admin Interface**: `https://your-domain.com/admin/`
- **Health Check**: `https://your-domain.com/health/`

## 📱 API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `GET /api/accounts/profile/` - User profile

### Posts & Comments
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create post
- `GET /api/posts/{id}/` - Get post details
- `POST /api/posts/{id}/like/` - Like post
- `POST /api/posts/{id}/unlike/` - Unlike post
- `GET /api/comments/` - List comments
- `POST /api/comments/` - Create comment

### Social Features
- `POST /api/accounts/follow/{user_id}/` - Follow user
- `POST /api/accounts/unfollow/{user_id}/` - Unfollow user
- `GET /api/feed/` - Get personalized feed

### Notifications
- `GET /api/notifications/` - List notifications
- `PATCH /api/notifications/{id}/mark-read/` - Mark as read
- `PATCH /api/notifications/mark-all-read/` - Mark all as read

## 🔒 Security Features

- Token-based authentication
- HTTPS enforcement in production
- Security headers (XSS, CSRF, etc.)
- Input validation and sanitization
- Rate limiting (configurable)

## 📈 Monitoring

- Health check endpoint: `/health/`
- Application logs: Check your hosting provider's logs
- Error tracking: Configure Sentry (optional)

## 🛠️ Maintenance

### Database Migrations
```bash
# Heroku
heroku run python manage.py migrate

# Docker
docker-compose exec web python manage.py migrate

# VPS
python manage.py migrate --settings=social_media_api.settings_production
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Creating Superuser
```bash
# Heroku
heroku run python manage.py createsuperuser

# Docker
docker-compose exec web python manage.py createsuperuser

# VPS
python manage.py createsuperuser --settings=social_media_api.settings_production
```

## 📞 Support

If you encounter issues:
1. Check the application logs
2. Verify environment variables
3. Test the health check endpoint
4. Review the deployment documentation

## 🎯 Next Steps

After successful deployment:
1. Set up domain and SSL certificate
2. Configure email service
3. Set up monitoring and alerts
4. Plan for scaling and backups
5. Configure CDN for static files (optional)

---

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)
