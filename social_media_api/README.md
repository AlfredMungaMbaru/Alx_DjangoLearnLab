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

### Posts and Comments Endpoints

#### Posts Management

##### List Posts
- **URL:** `GET /api/posts/`
- **Description:** Retrieve a paginated list of all posts
- **Authentication:** Token optional (public read access)
- **Query Parameters:**
  - `page`: Page number for pagination
  - `page_size`: Number of posts per page (max 100)
  - `search`: Search in title and content
  - `ordering`: Order by created_at, updated_at
  - `author`: Filter by author ID
- **Response:**
  ```json
  {
    "count": 25,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "My First Post",
        "content": "This is my first post content...",
        "author": {
          "id": 1,
          "username": "john_doe"
        },
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z",
        "comments_count": 5
      }
    ]
  }
  ```

##### Create Post
- **URL:** `POST /api/posts/`
- **Description:** Create a new post
- **Authentication:** Token required
- **Request Body:**
  ```json
  {
    "title": "My New Post",
    "content": "This is the content of my new post..."
  }
  ```
- **Response:**
  ```json
  {
    "id": 2,
    "title": "My New Post",
    "content": "This is the content of my new post...",
    "author": {
      "id": 1,
      "username": "john_doe"
    },
    "author_id": 1,
    "created_at": "2024-01-01T12:30:00Z",
    "updated_at": "2024-01-01T12:30:00Z",
    "comments": [],
    "comments_count": 0
  }
  ```

##### Get Post Detail
- **URL:** `GET /api/posts/{id}/`
- **Description:** Retrieve detailed information about a specific post including comments
- **Authentication:** Token optional
- **Response:**
  ```json
  {
    "id": 1,
    "title": "My First Post",
    "content": "This is my first post content...",
    "author": {
      "id": 1,
      "username": "john_doe"
    },
    "author_id": 1,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z",
    "comments": [
      {
        "id": 1,
        "content": "Great post!",
        "author": {
          "id": 2,
          "username": "jane_doe"
        },
        "author_id": 2,
        "created_at": "2024-01-01T12:15:00Z",
        "updated_at": "2024-01-01T12:15:00Z"
      }
    ],
    "comments_count": 1
  }
  ```

##### Update Post
- **URL:** `PUT/PATCH /api/posts/{id}/`
- **Description:** Update a post (only by author)
- **Authentication:** Token required (must be post author)
- **Request Body:**
  ```json
  {
    "title": "Updated Post Title",
    "content": "Updated post content..."
  }
  ```

##### Delete Post
- **URL:** `DELETE /api/posts/{id}/`
- **Description:** Delete a post (only by author)
- **Authentication:** Token required (must be post author)

##### Get Post Comments
- **URL:** `GET /api/posts/{id}/comments/`
- **Description:** Get all comments for a specific post (paginated)
- **Authentication:** Token optional

#### Comments Management

##### List Comments
- **URL:** `GET /api/comments/`
- **Description:** Retrieve a paginated list of all comments
- **Authentication:** Token optional
- **Query Parameters:**
  - `page`: Page number for pagination
  - `page_size`: Number of comments per page
  - `search`: Search in comment content
  - `post`: Filter by post ID
  - `author`: Filter by author ID
  - `ordering`: Order by created_at, updated_at

##### Create Comment
- **URL:** `POST /api/comments/`
- **Description:** Create a new comment on a post
- **Authentication:** Token required
- **Request Body:**
  ```json
  {
    "post": 1,
    "content": "This is my comment on the post..."
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "content": "This is my comment on the post...",
    "author": {
      "id": 1,
      "username": "john_doe"
    },
    "author_id": 1,
    "created_at": "2024-01-01T12:15:00Z",
    "updated_at": "2024-01-01T12:15:00Z"
  }
  ```

##### Get Comment Detail
- **URL:** `GET /api/comments/{id}/`
- **Description:** Retrieve detailed information about a specific comment
- **Authentication:** Token optional

##### Update Comment
- **URL:** `PUT/PATCH /api/comments/{id}/`
- **Description:** Update a comment (only by author)
- **Authentication:** Token required (must be comment author)

##### Delete Comment
- **URL:** `DELETE /api/comments/{id}/`
- **Description:** Delete a comment (only by author)
- **Authentication:** Token required (must be comment author)

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

## Post Model

The Post model represents user-generated content:

### Fields
- **author**: ForeignKey to User (who created the post)
- **title**: CharField with max 200 characters
- **content**: TextField for post content
- **created_at**: DateTimeField (auto-generated on creation)
- **updated_at**: DateTimeField (auto-updated on modification)

### Relationships
- **author**: Many-to-one relationship with User
- **comments**: One-to-many relationship with Comment (reverse relation)

## Comment Model

The Comment model represents user comments on posts:

### Fields
- **post**: ForeignKey to Post (which post this comment belongs to)
- **author**: ForeignKey to User (who wrote the comment)
- **content**: TextField for comment content
- **created_at**: DateTimeField (auto-generated on creation)
- **updated_at**: DateTimeField (auto-updated on modification)

### Relationships
- **post**: Many-to-one relationship with Post
- **author**: Many-to-one relationship with User

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