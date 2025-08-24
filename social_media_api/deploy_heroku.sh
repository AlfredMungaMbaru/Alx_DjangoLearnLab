#!/bin/bash

# Heroku Deployment Script for Social Media API

echo "🚀 Starting Heroku deployment for Social Media API..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "❌ Please log in to Heroku first:"
    echo "heroku login"
    exit 1
fi

# App name (change this to your preferred app name)
APP_NAME="social-media-api-$(whoami)-$(date +%s)"
echo "📱 Creating Heroku app: $APP_NAME"

# Create Heroku app
heroku create $APP_NAME

# Add PostgreSQL addon
echo "🗄️  Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:essential-0 --app $APP_NAME

# Add Redis addon for caching
echo "🔄 Adding Redis for caching..."
heroku addons:create heroku-redis:mini --app $APP_NAME

# Set environment variables
echo "⚙️  Setting environment variables..."
heroku config:set DEBUG=False --app $APP_NAME
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') --app $APP_NAME
heroku config:set SECURE_SSL_REDIRECT=True --app $APP_NAME
heroku config:set SESSION_COOKIE_SECURE=True --app $APP_NAME
heroku config:set CSRF_COOKIE_SECURE=True --app $APP_NAME

# Deploy the application
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Prepare for Heroku deployment" || echo "No changes to commit"
git push heroku main

# Run migrations
echo "📊 Running database migrations..."
heroku run python manage.py migrate --app $APP_NAME

# Create superuser (optional)
read -p "Do you want to create a superuser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "👤 Creating superuser..."
    heroku run python manage.py createsuperuser --app $APP_NAME
fi

# Open the app
echo "✅ Deployment complete!"
echo "🌐 App URL: https://$APP_NAME.herokuapp.com"
echo "📊 Admin URL: https://$APP_NAME.herokuapp.com/admin"

heroku open --app $APP_NAME

echo "📋 Useful commands:"
echo "heroku logs --tail --app $APP_NAME  # View logs"
echo "heroku run python manage.py shell --app $APP_NAME  # Django shell"
echo "heroku config --app $APP_NAME  # View environment variables"
