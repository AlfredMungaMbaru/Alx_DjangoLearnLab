from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for the CustomUser model.
    Handles user creation and queries while managing the additional fields.
    """
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a regular user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The Username field must be set')
        
        # Normalize email if provided
        if email:
            email = self.normalize_email(email)
        
        # Set default values for extra fields
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        # Create user instance
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given username, email, and password.
        """
        # Set required fields for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Adds additional fields for date of birth and profile photo.
    """
    
    # Additional custom fields
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        help_text="User's date of birth"
    )
    
    profile_photo = models.ImageField(
        upload_to='profile_photos/', 
        null=True, 
        blank=True,
        help_text="User's profile photo"
    )
    
    # Use our custom manager
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    @property
    def age(self):
        """
        Calculate and return the user's age based on date_of_birth.
        """
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def get_profile_photo_url(self):
        """
        Return the URL of the profile photo or a default placeholder.
        """
        if self.profile_photo:
            return self.profile_photo.url
        return '/static/images/default-profile.png'  # You can add a default image


class Book(models.Model):
    """
    Book model that demonstrates how to reference the custom user model.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    
    # Reference to the custom user model using settings.AUTH_USER_MODEL
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        permissions = [
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author}"


class Library(models.Model):
    """
    Library model that demonstrates many-to-many relationship with custom user model.
    """
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    
    # Many-to-many relationship with the custom user model
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        related_name='libraries'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'
    
    def __str__(self):
        return self.name


class Membership(models.Model):
    """
    Intermediate model for the many-to-many relationship between Library and CustomUser.
    """
    MEMBERSHIP_TYPES = [
        ('regular', 'Regular'),
        ('premium', 'Premium'),
        ('student', 'Student'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPES, default='regular')
    joined_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'library']
        ordering = ['-joined_date']
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
    
    def __str__(self):
        return f"{self.user.username} - {self.library.name} ({self.membership_type})"


class BookReview(models.Model):
    """
    Book review model that demonstrates another use case for the custom user model.
    """
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['book', 'reviewer']
        ordering = ['-created_at']
        verbose_name = 'Book Review'
        verbose_name_plural = 'Book Reviews'
    
    def __str__(self):
        return f"{self.book.title} - {self.rating} stars by {self.reviewer.username}"
