from django.db import models
from django.conf import settings
from django.utils import timezone


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
