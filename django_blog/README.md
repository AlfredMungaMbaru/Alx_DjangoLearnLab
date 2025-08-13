# Django Blog Project

A comprehensive Django blog application built as part of the ALX Django learning lab.

## Features

- **User Authentication**: Complete registration, login, logout, and profile management system
- **Post Management**: Create, read, update, and delete blog posts through admin interface
- **User Profiles**: Users can view and edit their profile information and see their posts
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Pagination**: Efficient handling of multiple blog posts
- **Admin Interface**: Django admin panel for content management
- **Static Files**: CSS and JavaScript for enhanced user experience
- **Security**: CSRF protection, secure password handling, and session management

## Project Structure

```
django_blog/
├── blog/                           # Main blog application
│   ├── migrations/                 # Database migrations
│   ├── static/blog/               # Static files (CSS, JS)
│   │   ├── css/
│   │   │   └── style.css          # Custom styles
│   │   └── js/
│   │       └── main.js            # JavaScript functionality
│   ├── templates/blog/            # HTML templates
│   │   ├── base.html              # Base template
│   │   ├── post_list.html         # Blog post list view
│   │   └── post_detail.html       # Individual post view
│   ├── admin.py                   # Admin configuration
│   ├── models.py                  # Database models
│   ├── urls.py                    # URL patterns
│   └── views.py                   # View functions
├── django_blog/                   # Project configuration
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Main URL configuration
│   └── wsgi.py                    # WSGI configuration
├── manage.py                      # Django management script
├── requirements.txt               # Project dependencies
└── README.md                      # This file
```

## Models

### Post Model
- **title**: CharField (max_length=200) - The title of the blog post
- **content**: TextField - The main content of the blog post
- **published_date**: DateTimeField (auto_now_add=True) - Automatically set when post is created
- **author**: ForeignKey to User - Links posts to their authors

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd django_blog
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main blog: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Default Admin Credentials

For demonstration purposes, a default superuser has been created:
- **Username:** admin
- **Password:** admin123
- **Email:** admin@example.com

**⚠️ Note:** Change these credentials in production environments!

## Usage

### Authentication System

#### User Registration
1. Navigate to `/register/` or click "Register" in the navigation
2. Fill out the registration form with username, email, and password
3. Optionally provide first and last name
4. Submit the form to create your account and automatically log in

#### User Login
1. Navigate to `/login/` or click "Login" in the navigation
2. Enter your username and password
3. Submit to log in and access personalized features

#### Profile Management
1. While logged in, navigate to `/profile/` or click "Profile"
2. View your account information and statistics
3. Update your profile details as needed
4. See a list of all your blog posts

### Viewing Blog Posts
- Navigate to the home page to see all published blog posts
- Click on any post title to view the full content
- Use pagination controls to navigate through multiple pages of posts

### Managing Posts (Admin)
1. Access the admin interface at `/admin/`
2. Log in with your superuser credentials
3. Click on "Posts" to manage blog posts
4. Add, edit, or delete posts as needed

## Customization

### Styling
- Modify `blog/static/blog/css/style.css` to customize the appearance
- The project uses Bootstrap 5 for responsive design

### Templates
- Edit templates in `blog/templates/blog/` to change the layout
- `base.html` contains the common structure used by all pages

### Functionality
- Add new features by extending models in `blog/models.py`
- Create new views in `blog/views.py`
- Add URL patterns in `blog/urls.py`

## Technologies Used

- **Django 5.2.5**: Web framework
- **SQLite**: Default database (easily configurable for other databases)
- **Bootstrap 5**: CSS framework for responsive design
- **HTML5 & CSS3**: Frontend markup and styling
- **JavaScript**: Interactive features

## File Structure Details

### Static Files
- **CSS**: Located in `blog/static/blog/css/`
- **JavaScript**: Located in `blog/static/blog/js/`
- **Images**: Can be added to `blog/static/blog/images/`

### Templates
- **Base Template**: Provides common structure (navigation, footer)
- **Post List**: Displays paginated list of blog posts
- **Post Detail**: Shows individual blog post with full content

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is created for educational purposes as part of the ALX Django learning curriculum.

## Contact

For questions or support, please contact the development team.
