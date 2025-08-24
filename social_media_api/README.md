# Social Media API

A Django REST Framework-based social media API with user authentication, custom user models, and token-based authentication.

## Project Overview

This project provides a foundation for a social media platform with the following features:
- Custom user model with bio, profile picture, and follower functionality
- Token-based authentication
- User registration and login endpoints
- User profile management

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 5.2+
- Django REST Framework

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework Pillow
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication Endpoints

#### User Registration
- **URL:** `POST /api/accounts/register/`
- **Description:** Register a new user account
- **Request Body:**
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "bio": "Hello, I'm John!",
    "profile_picture": null
  }
  ```
- **Response:**
  ```json
  {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "bio": "Hello, I'm John!",
      "profile_picture": null,
      "followers_count": 0,
      "following_count": 0,
      "date_joined": "2024-01-01T12:00:00Z"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "message": "User registered successfully"
  }
  ```

#### User Login
- **URL:** `POST /api/accounts/login/`
- **Description:** Authenticate user and retrieve token
- **Request Body:**
  ```json
  {
    "username": "john_doe",
    "password": "securepassword123"
  }
  ```
- **Response:**
  ```json
  {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "bio": "Hello, I'm John!",
      "profile_picture": null,
      "followers_count": 0,
      "following_count": 0,
      "date_joined": "2024-01-01T12:00:00Z"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "message": "Login successful"
  }
  ```

#### User Profile
- **URL:** `GET/PUT /api/accounts/profile/`
- **Description:** Retrieve or update user profile
- **Authentication:** Token required
- **Headers:**
  ```
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
  ```
- **GET Response:**
  ```json
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "bio": "Hello, I'm John!",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0,
    "date_joined": "2024-01-01T12:00:00Z"
  }
  ```

## User Model

The custom user model extends Django's `AbstractUser` with additional fields:

### Fields
- **username**: Unique username (inherited)
- **email**: Email address (inherited)
- **password**: Encrypted password (inherited)
- **bio**: Text field for user biography (max 500 characters)
- **profile_picture**: Image field for profile picture
- **followers**: Many-to-many relationship to other users (asymmetrical)

### Relationships
- **followers**: Users who follow this user
- **following**: Users this user follows (reverse relation)

## Authentication

The API uses Django REST Framework's Token Authentication:

1. **Registration/Login**: Returns a token upon successful authentication
2. **Protected Endpoints**: Include the token in the Authorization header:
   ```
   Authorization: Token <your-token-here>
   ```

## Testing with Postman/cURL

### Register a new user:
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "bio": "Test user bio"
  }'
```

### Login:
```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Get profile (replace TOKEN with actual token):
```bash
curl -X GET http://localhost:8000/api/accounts/profile/ \
  -H "Authorization: Token TOKEN"
```

## Project Structure

```
social_media_api/
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # CustomUser model
│   ├── serializers.py     # DRF serializers
│   ├── urls.py           # Account URLs
│   └── views.py          # Authentication views
├── social_media_api/
│   ├── __init__.py
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py
├── manage.py
└── README.md
```

## Next Steps

This foundation provides the base for expanding the social media API with additional features such as:
- Posts and content management
- Comments and interactions
- Real-time notifications
- Follow/unfollow functionality
- Media file handling
- Search and discovery features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.